import logging
import time
import csv
import execjs
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor, as_completed

proxies = {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the environment and session
parser = etree.HTMLParser(encoding="utf-8")
node = execjs.get()
with open("./M2_decode.js", "r", encoding="utf-8") as f:
    js_ctx = node.compile(f.read())

username = js_ctx.call("RSA_Public_Encrypt", "19504667538")
password = js_ctx.call("RSA_Public_Encrypt", "Chqteng1234")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
}

data = {
    'username': username,
    'password': password,
    'rememberMe': 'false',
    'app': 'robo_pc',
    'sourceApp': 'robo_pc',
}

session = requests.Session()
response = session.post('https://gw.datayes.com/usermaster/authenticate/web.json', data=data, headers=headers , proxies= proxies)

# Check if authentication was successful
if response.status_code != 200:
    logging.error("Authentication failed with status code %d", response.status_code)
else:
    logging.info("Successfully authenticated.")


# Parse the detailed page
def parse_detail_page(res):
    try:
        link = res['data']['downloadUrl']
        stk_id = res['data']['stockId']
        time.sleep(0.5)
        return [stk_id, link]
    except KeyError as e:
        logging.error(f"Missing key in response: {e}")
        return None


# Scrape page
def scrape_page(url):
    try:
        response = session.get(url, headers=headers , proxies= proxies )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching page {url}: {e}")
        return None


# Index page to fetch URLs
def index_page(index):
    url = f"https://gw.datayes.com/rrp_adventure/web/search?pageNow={index}&authorId=&isOptional=false&orgName=&reportType=COMPANY&secCodeList=&reportSubType=&industry=&ratingType=&pubTimeStart=20140921&pubTimeEnd=20240921&type=EXTERNAL_REPORT&pageSize=40&sortOrder=desc&query=&minPageCount=&maxPageCount="
    try:
        res = session.get(url, headers=headers , proxies= proxies)
        res.raise_for_status()
        result = res.json()
        items = result['data']['list']
        return [item['data']['id'] for item in items]
    except requests.RequestException as e:
        logging.error(f"Error fetching index page {index}: {e}")
        return []


# Save data to CSV
def save_data(res, csv_writer):
    if res:
        csv_writer.writerow(res)


# Main scraping logic with concurrency
def main():
    with open('./result.csv', 'w', newline='', encoding="utf-8") as f:
        csv_writer = csv.writer(f)

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {}

            for i in range(6, 11):
                detail_urls = index_page(i)

                if detail_urls:
                    for detail_url in detail_urls:
                        full_url = f"https://gw.datayes.com/rrp_adventure/web/externalReport/{detail_url}"
                        future = executor.submit(scrape_page, full_url)
                        future_to_url[future] = full_url

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    detail_res = future.result()
                    if detail_res:
                        result = parse_detail_page(detail_res)
                        save_data(result, csv_writer)
                        logging.info(f"Successfully got data for {result}")
                except Exception as e:
                    logging.error(f"Error processing page {url}: {e}")


if __name__ == '__main__':
    main()
