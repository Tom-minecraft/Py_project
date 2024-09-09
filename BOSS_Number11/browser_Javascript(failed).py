# Target : https://spa2.scrape.center
import requests
from playwright.sync_api import sync_playwright

proxies = {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}

BASE_URL = "https://spa2.scrape.center"
INDEX_URL = BASE_URL + "/api/movie/?limit={limit}&offset={offset}&token={token}"
TOTAL_PAGE = 10
limit = 10
context = sync_playwright().start()
browser = context.chromium.launch()
page = browser.new_page()
page.route("./js/chunk-10192a00.243cb8b7.js",lambda route : route.fulfill(path="./js/chunk-10192a00.243cb8b7.js"))
page.goto(BASE_URL)

def get_token(offset):
    result = page.evaluate("""() =>{ 
    return window.enc("%s","%s")
    }""" %('/api/movie',offset))
    return result


for i in range(TOTAL_PAGE):
    offset = i * limit
    token = get_token(offset)
    index_url = INDEX_URL.format(limit=limit, offset=offset, token=token)
    response = requests.get(index_url,proxies=proxies)
    print(response.json)
