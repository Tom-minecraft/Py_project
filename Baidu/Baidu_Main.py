import logging
from lxml import etree
import requests
import pprint
from DrissionPage import ChromiumPage
proxies = {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.baidu.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.baidu.com/',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {

}

BASE_URL = 'https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F&sms=5'
TARGET_URL =' https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_9469499570077154318%22%7D&n_type=-1&p_from=-1'
username = 18249555724
password = "chqteng1234"
page = ChromiumPage()

def login_then_get_cookies(username, password):
    page.get(BASE_URL)
    page.wait(5)
    page.ele("#TANGRAM__PSP_3__userName").input(username)
    page.ele("#TANGRAM__PSP_3__password").input(password)
    try:
        page.ele("#TANGRAM__PSP_3__submit").click()
        page.wait(3)  # 确保页面加载完成
        cookies = get_cookies()
        page.close()
        return cookies
    except Exception as e:
        print(f'Failed: {e}')
        return False


def get_cookies():
    cookie_dict = {cookie['name']: cookie['value'] for cookie in page.cookies()}
    return cookie_dict







def Get_Base_html():
    logging.info("Sraping %s" % BASE_URL)
    try:
        response = requests.get(BASE_URL,proxies=proxies , headers=headers)
        if response.status_code == 200:
            return response.text
        logging.error("Failed:Wrong Status Code %s" % response.status_code)
    except requests.RequestException as e:
        logging.error("Something went wrong: %s" % e)

# def Parse_Base_html(html):
#     HTML = etree.HTML(html, etree.HTMLParser())











def main():
    cookies = login_then_get_cookies(username, password)
    params = {
        'context': '{"nid":"news_9469499570077154318"}',
        'n_type': '-1',
        'p_from': '-1',
    }

    response = requests.get('https://mbd.baidu.com/newspage/data/landingsuper', params=params, cookies=cookies , proxies=proxies , headers=headers)
    pprint.pprint(response.text)


if __name__ == '__main__':
    main()


