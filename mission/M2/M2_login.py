import logging
import time

logging.basicConfig(level=logging.INFO,format='%(asctime)s%(levelname)s - %(message)s')
import csv
import execjs
import requests


from lxml import etree
parser = etree.HTMLParser(encoding="utf-8")
node = execjs.get()
with open("./M2_decode.js", "r", encoding="utf-8") as f:
    js_ctx = node.compile(f.read())

username = js_ctx.call("RSA_Public_Encrypt", "19504667538")
password = js_ctx.call("RSA_Public_Encrypt", "Minecraft1234")

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
}



data = {
    'username': username,
    'password': password,
    'rememberMe': 'false',
    'app': 'robo_pc',
    'sourceApp': 'robo_pc',
}

response = requests.post('https://gw.datayes.com/usermaster/authenticate/web.json',  data=data, headers=headers)

cookies = response.cookies
session = requests.session()
for name, value in cookies.items():
    session.cookies.set(name, value)

def parse_detail_page(res):
    link = res['data']['downloadUrl']
    stk_id = res['data']['stockId']
    time.sleep(0.5)
    return [stk_id , link]
def scrape_page(url):
    response = session.get(url,headers=headers)
    return response.json()



def index_page(index):
    url = f"https://gw.datayes.com/rrp_adventure/web/search?pageNow={index}&authorId=&isOptional=false&orgName=&reportType=COMPANY&secCodeList=&reportSubType=&industry=&ratingType=&pubTimeStart=20140921&pubTimeEnd=20240921&type=EXTERNAL_REPORT&pageSize=40&sortOrder=desc&query=&minPageCount=&maxPageCount="
    res = session.get(url,headers= headers)
    result = res.json()
    items = result['data']['list']
    indices = [item['data']['id'] for item in items]
    container = []
    for index in indices:
        detail_url = f"https://gw.datayes.com/rrp_adventure/web/externalReport/{index}"

        container.append(detail_url)
    return container

def save_data(res):
    csv_writer = csv.writer(f)
    csv_writer.writerow(res)

f = open('./result.csv', 'w',newline='', encoding="utf-8")
def main():
    for i in range(1,251):
        detail_urls = index_page(i)
        for detail_url in detail_urls:
            detail_res = scrape_page(detail_url)
            result = parse_detail_page(detail_res)
            save_data(result)
            logging.info("Successfully got : %s" % result)



if __name__ == '__main__':
    main()