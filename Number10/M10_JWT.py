import requests
from urllib.parse import urljoin

BASE_URL = 'https://login3.scrape.center/'
LOGIN_URL = urljoin(BASE_URL, 'api/login')
INDEX_URL = urljoin(BASE_URL, 'api/book')
USERNAME = 'admin'
PASSWORD = 'admin'
proxy = {
    'http': '127.0.0.1:7897',
    'https': '127.0.0.1:7897',
}
response_login = requests.post(LOGIN_URL, json={
    'username': USERNAME,
    'password': PASSWORD,
},proxies=proxy)

data = response_login.json()
print(data)
jwt = data.get('token')
print(jwt)
headers = {'Authorization': f'jwt {jwt}'}
response_index = requests.get(INDEX_URL,params={'limit':18,'offset':0},headers=headers,proxies=proxy)
print(response_index.status_code)
print(response_index.json())