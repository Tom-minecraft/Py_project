from selenium import webdriver
from urllib.parse import urljoin
import time
import requests
BASE_URL = 'https://login2.scrape.center/'
LOGIN_URL = urljoin(BASE_URL , 'login')
INDEX_URL = urljoin(BASE_URL ,'page/1')
USERNAME = 'admin'
PASSWORD = 'admin'
proxy={
    'http':'127.0.0.1:7897',
    'https':'127.0.0.1:7897'
}
browser = webdriver.Chrome()
browser.get(BASE_URL)
browser.find_element("xpath","//input[@name='username']").send_keys(USERNAME)
browser.find_element("xpath","//input[@name='password']").send_keys(PASSWORD)
browser.find_element("xpath","//input[@type='submit']").click()

cookies = browser.get_cookies()
print(cookies)
browser.quit()
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])
response_index = session.get(INDEX_URL,proxies=proxy)
print(response_index.status_code)