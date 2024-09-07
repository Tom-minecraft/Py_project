import logging

import requests
from urllib.parse import urljoin
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
BASE_URL = 'https://login2.scrape.center/'
LOGIN_URL = urljoin(BASE_URL , 'login')
INDEX_URL = urljoin(BASE_URL ,'page/1')
USERNAME = 'admin'
PASSWORD = 'admin'
proxy = {
    'http': None,
    'https': None
}

data={
    'username': USERNAME,
    'password': PASSWORD,
}
session = requests.Session()
response_login = session.post(LOGIN_URL,data=data,proxies=proxy)
response_index = session.get(INDEX_URL,proxies=proxy)
print(response_index.status_code)
print(response_index.url)

