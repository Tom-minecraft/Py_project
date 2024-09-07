
"""---------------requests-----------------"""
import requests
import logging
logging.basicConfig(level=logging.DEBUG)
proxy = '127.0.0.1:7897'
proxies = {
    'http': 'http://'+ proxy,
    'https': 'http://'+ proxy,
}
try:
    response = requests.get('http://www.httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.RequestException as e:
    print(e)
