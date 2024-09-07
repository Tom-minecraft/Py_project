import ddddocr
import requests
from DrissionPage import ChromiumPage
from PIL import Image

# 初始化 OCR 和浏览器
ocr = ddddocr.DdddOcr(beta=True)  # 使用第二套OCR模型
page = ChromiumPage()

# 登录页面的 URL
url_login = 'https://authserver.suibe.edu.cn/authserver/login?service=https%3A%2F%2Fnbkjw.suibe.edu.cn%2Fstudent%2Fsso%2Flogin'


# 登录函数
def login(username, password):
    # 打开登录页面
    page.get(url_login)
    page.wait(5)

    # 输入用户名和密码
    page("#username").input(username)
    page("#password").input(password)

    # 获取验证码图片元素
    captcha_element = page('#captchaImg')

    # 获取整个页面的截图
    page.screenshot('full_page.png')  # 保存整个页面为图片

    # 获取验证码元素的位置信息
    location = captcha_element.location
    size = captcha_element.size

    # 打开页面截图并裁剪出验证码部分
    image = Image.open('full_page.png')
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']
    captcha_image = image.crop((left, top, right, bottom))
    captcha_image.save('captcha.png')  # 保存验证码图片

    # 读取验证码为二进制字节流
    with open('captcha.png', 'rb') as img_file:
        image_bytes = img_file.read()

    # 使用 ddddocr 识别验证码
    result = ocr.classification(image_bytes)
    print('识别的验证码:', result)

    # 输入验证码
    page("#captchaResponse").input(result)

    # 尝试点击登录
    try:
        page.ele('x://button').click()
        page.wait(3)  # 确保页面加载完成
    except Exception as e:
        print(f'登录失败: {e}')
        return False
    return True


# 获取登录后的 cookies 并返回
def get_cookies():
    cookie_dict = {cookie['name']: cookie['value'] for cookie in page.cookies()}
    print('获取到的Cookies:', cookie_dict)
    return cookie_dict


# 通过 requests 进行页面抓取
def fetch_protected_page(url, headers, cookies):
    try:
        response = requests.get(url=url, headers=headers, cookies=cookies, allow_redirects=False)
        print('响应状态码:', response.status_code)
        return response.text
    except Exception as e:
        print(f'抓取页面失败: {e}')
        return None


if __name__ == '__main__':
    username = '23060080'
    password = 'Sgl197683!'

    # 尝试登录
    if login(username, password):
        # 获取 Cookies
        cookies = get_cookies()

        # 设置请求头
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "nbkjw.suibe.edu.cn",
            "Referer": "https://nbkjw.suibe.edu.cn/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }

        # 访问需要登录的页面
        url_protected = 'https://nbkjw.suibe.edu.cn/student/home'
        content = fetch_protected_page(url_protected, headers, cookies)
        if content:
            print(content)
    else:
        print("登录失败，无法继续后续操作")
