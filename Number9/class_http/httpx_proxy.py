import httpx
import logging
logging.basicConfig(level=logging.INFO)
proxy = '127.0.0.1:7897'
proxies = {
    'http://': 'http://'+ proxy,
    'https://': 'https://'+ proxy,
}

with httpx.Client(proxies=proxies) as client:
    response = client.get(url='http://httpbin.org/get')
    print(response.text)