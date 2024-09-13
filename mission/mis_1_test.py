import logging

import pymongo
import requests

import pymysql
db = pymysql.connect(host='localhost', port=3306,user='root', passwd='chqteng1234', db='spider')
cursor = db.cursor()




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s : %(message)s')

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

# URL for getting the parameters
url = "https://gs.sac.net.cn/publicity/getSponsorAList"


def get_param(url):
    logging.info('Fetching parameters from: %s', url)
    try:
        response = requests.get(url, proxies=proxies, headers=headers)
        if response.status_code == 200:
            try:
                # Parse JSON response
                data = response.json()

                # Check for success response
                if isinstance(data, dict) and data.get('success') and data.get('code') == 20000:
                    sponsor_list = data.get('data', {})
                    uuids = []

                    # Extract UUIDs
                    for sponsor_data in sponsor_list.values():
                        for item in sponsor_data:
                            uuids.append(item['uuid'])
                    return uuids
                else:
                    logging.error(f"Request failed: {data.get('message', 'Unknown error')}")
            except requests.exceptions.JSONDecodeError:
                logging.error("Response is not valid JSON")
        else:
            logging.error(f"Failed to fetch parameters, status code: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Error while fetching parameters: {e}", exc_info=True)

    return []


def scrape_page(param):
    logging.info('Scraping detail page with uuid: %s', param)
    try:
        detail_url = "https://gs.sac.net.cn/publicity/getSponsorDetail"
        data = {'uuid': param}
        response = requests.post(detail_url, data=data, proxies=proxies, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Failed to scrape page, status code: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Error while scraping page: {e}", exc_info=True)

    return None


def parse_page(data):
    if data and 'data' in data and 'data' in data['data']:
        name = data['data']['data']["name"]
        gender = data['data']['data']["gender"]
        orgName = data['data']['data']['orgName']
        certifNo = data['data']['data']['certifNo']
        pracCtegName = data['data']['data']['pracCtegName']
        edu = data['data']['data']['edu']
        regDate = data['data']['data']['regDate']
        return {
            "name": name,
            "gender": gender,
            "organization": orgName,
            "registration_number": certifNo,
            "registration_category": pracCtegName,
            "education": edu,
            "registration_date": regDate
        }
    logging.error("Invalid data format received")
    return None

def save_data(data):
    table = "personnel_registration"
    keys = ','.join(data.keys())
    values = ','.join(['%s'] * len(data))
    sql = f'INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '
    update = ','.join([f'{key}=%s' for key in data])
    final_sql = sql + update
    try:
        cursor.execute(final_sql, tuple(data.values()) * 2)
        db.commit()
    except Exception as e:
        logging.error(e)
        db.rollback()

def main():
    uuids = get_param(url)
    if not uuids:
        logging.error("No UUIDs found")
        return

    for uuid in uuids:
        data = scrape_page(uuid)
        if data:
            result = parse_page(data)
            logging.info("Successfully got data : %s", result)
            save_data(result)
            logging.info("Successfully saved data")


if __name__ == '__main__':
    main()
    db.close()
