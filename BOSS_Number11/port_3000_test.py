import requests



item = {
    "name": "凯文-杜兰特",
    "image": "durant.png",
    "birthday": "1988-09-29",
    "height": "208cm",
    "weight": "108.9KG"
}
proxy = '127.0.0.1:7897'
proxies = {
    'http': 'http://'+ proxy,
    'https': 'http://'+ proxy,
}
url = "http://127.0.0.1:3000"
try:
    response = requests.post(url, json=item, proxies=proxies)
    print(response.text)
except Exception as e:
    print(e)