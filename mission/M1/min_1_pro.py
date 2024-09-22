import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s : %(message)s')
import requests

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://gs.sac.net.cn',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://gs.sac.net.cn/pages/registration/branch-publicity-tableAperson.html?r2SS_IFjjk=1614059640944451991',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


proxies = {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


url = "https://gs.sac.net.cn/publicity/getSponsorAList"



def get_param(url):
    # 发送请求
    response = requests.get(url, proxies=proxies, headers=headers)
    if response.status_code == 200:
        try:
            # 解析 JSON 数据
            data = response.json()



            # 检查返回的状态
            if isinstance(data, dict) and data.get('success') and data.get('code') == 20000:
                # 提取关键数据
                sponsor_list = data['data']

                if isinstance(data['data'], dict):
                    uuids = []
                    for sponsor in sponsor_list.items():
                        sponsor_data = sponsor[1]
                        for item in sponsor_data:
                            uuid = item['uuid']
                            uuids.append(uuid)
                    return uuids



            else:
                print(f"请求失败: {data.get('message', '未知错误')}")
        except requests.exceptions.JSONDecodeError:
            print("响应不是有效的 JSON 格式")
    else:
        print(f"请求失败，状态码: {response.status_code}")

def scrape_page(param):
    logging.info('Scraping %s',url)
    try:
        data = {'uuid':param}
        response = requests.post(url, data=data,proxies=proxies, headers=headers)
        if response.status_code == 200:
            return response.json()
        logging.error("Failed ! Status code :%s ", response.status_code)
    except requests.RequestException :
        logging.error("Something went wrong : ",exc_info=True )

def parse_page(data):
    name = data['data']['data'][0]['name']
    return name

def main():
    uuids = get_param(url)
    for uuid in uuids:
        data = scrape_page(uuid)
        result = parse_page(data)
        print(result)








if __name__ == '__main__':
    main()