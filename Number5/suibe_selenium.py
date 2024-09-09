import logging
import re
import time
from io import BytesIO
import requests
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import tesserocr
from PIL import Image
from retrying import retry
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import execjs
import pymongo
import ddddocr
ocr = ddddocr.DdddOcr()

client = pymongo.MongoClient('localhost', 27017)
db = client.Mine
collection = db.Schedule

# 日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 执行JS文件
node = execjs.get()
_p1 = 'NeM7Jlflm79r3LJ2'
pwd = 'Sgl197683!'
with open('suibe_decode.js', 'r', encoding="utf-8") as f:
    ctx = f.read()
js_ctx = node.compile(ctx)
password = js_ctx.call("encryptAES", pwd, _p1)
logging.info("Password encryption complete.")

# 代理配置
proxies = {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}

# 请求头配置
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://authserver.suibe.edu.cn',
    'Referer': 'https://authserver.suibe.edu.cn/authserver/login?service=https%3A%2F%2Fnbkjw.suibe.edu.cn%2Fstudent%2Fsso%2Flogin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

def save_data(data):
    collection.update_one({
        'name': data.get('course').get('nameZh')
    }, {
        '$set': data
    }, upsert=True)

# 图像预处理函数
# def preprocess(image):
#     image_process = image.convert('L')
#     array = np.array(image_process)
#     threshold = np.mean(array) - 20  # 动态阈值调整
#     array = np.where(array > threshold, 255, 0)
#     image_process = Image.fromarray(array.astype('uint8'))
#     return image_process

# 重试机制：处理登录和获取Cookies
@retry(stop_max_attempt_number=5, retry_on_result = lambda x : x is False)
def selenium_login_and_get_cookies(browser):
    try:
        browser.get('https://authserver.suibe.edu.cn/authserver/login?service=https%3A%2F%2Fnbkjw.suibe.edu.cn%2Fstudent%2Fsso%2Flogin')

        # 输入用户名和密码
        browser.find_element(By.XPATH, '//*[@id="username"]').send_keys('23060080')
        browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('Sgl197683!')

        # 处理验证码
        captcha = browser.find_element(By.XPATH, '//*[@id="captchaImg"]')
        image = Image.open(BytesIO(captcha.screenshot_as_png))
        captcha_result = ocr.classification(image)

        # image_result = preprocess(image)
        # captcha_result = tesserocr.image_to_text(image_result)
        # captcha_result = re.sub('[^A-Za-z0-9]', '', captcha_result)

        # 获取动态字段
        lt = browser.find_element(By.NAME, 'lt').get_attribute('value')
        execution = browser.find_element(By.NAME, 'execution').get_attribute('value')

        # 输入验证码
        browser.find_element(By.XPATH, '//*[@id="captchaResponse"]').send_keys(captcha_result)

        # 提交登录表单
        browser.find_element(By.XPATH, '//*[@id="casLoginForm"]/p[5]/button').click()

        # 等待页面加载并获取 Cookies
        WebDriverWait(browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="home-page"]/section/div[1]/div[1]/div/div[1]/div/span[1]')
        ))
        time.sleep(5)
        cookies = browser.get_cookies()
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}

        return cookie_dict, captcha_result, lt, execution
    except TimeoutException:
        logging.warning("Timeout while waiting for the page to load.")
        return False
    except Exception as e:
        logging.error(f"Unexpected error during login: {e}")
        return False

# 使用 requests 发送表单并抓取内容
def scrape_with_requests(cookie_dict, captcha_result, lt, execution):
    data = {
        'username': '23060080',
        'password': password,
        'captchaResponse': captcha_result,
        'lt': lt,
        'dllt': 'userNamePasswordLogin',
        'execution': execution,
        '_eventId': 'submit',
        'rmShown': '1',
    }

    session = requests.Session()
    for name, value in cookie_dict.items():
        session.cookies.set(name, value)

    try:
        url = "https://nbkjw.suibe.edu.cn/student/for-std/course-table/get-data?semesterId=53&dataId=434729&bizTypeId=2"

        response = session.get(url, headers=headers)
        response.raise_for_status()  # 检查 HTTP 响应是否成功
        return response.json()
    except requests.exceptions.Timeout:
        logging.error("Request timed out.")
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Error occurred during the request: {err}")
    return None

if __name__ == '__main__':
    # 启动无头浏览器
    options = webdriver.ChromeOptions()

    browser = webdriver.Chrome()

    try:
        # Step 1: 使用 Selenium 获取 Cookies、验证码、以及动态字段
        cookies, captcha_result, lt, execution = selenium_login_and_get_cookies(browser)

        if cookies:
            # Step 2: 使用 requests 提交表单并抓取页面
            session_response = scrape_with_requests(cookies, captcha_result, lt, execution)
            if session_response:
                for data in session_response.get('lessons'):
                    logging.info(f"lesson:{data}")
                    save_data(data)
                    logging.info("Successfully got it")


            else:
                logging.error("Failed to fetch session content.")
        else:
            logging.error("Failed to get cookies and fields from Selenium.")
    except Exception as e:
        logging.error(e)
    finally:
        # 关闭浏览器
        browser.quit()
