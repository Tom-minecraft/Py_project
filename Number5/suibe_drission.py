from DrissionPage import ChromiumPage
import ddddocr
from PIL import Image
from io import BytesIO



ocr = ddddocr.DdddOcr(beta=True)
username = "23060080"
password = "Sgl197683!"
url_login = 'https://authserver.suibe.edu.cn/authserver/login?service=https%3A%2F%2Fnbkjw.suibe.edu.cn%2Fstudent%2Fsso%2Flogin'

page = ChromiumPage()
page.get(url_login)
page("#username").input(username)
page("#password").input(password)
captcha_element = page('#captchaImg')
captcha_element.get_screenshot("captcha.png")
with open('captcha.png', 'rb') as f:
    captcha_image = f.read()

result = ocr.classification(captcha_image)
print(result)
page("#captchaResponse").input(result)
page.ele('x://button').click()
cookie_dict = {cookie['name']: cookie['value'] for cookie in page.cookies()}
print('获取到的Cookies:', cookie_dict)
