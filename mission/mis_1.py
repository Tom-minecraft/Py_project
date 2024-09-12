import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s : %(message)s')
import requests

import pymysql
db = pymysql.connect(host="localhost", port=3306, user="root", passwd="chqteng1234")
cursor = db.cursor()
cursor.execute("use spider")
sql = """
INSERT INTO sponsor_info (id, name, orgAbbrName, prjCnt, profLvlSituCode, badSinhonClassifName)
VALUES (%s,%s,%s,%s,%s,%s)
ON DUPLICATE KEY UPDATE
name = VALUES(name),
orgAbbrName = VALUES(orgAbbrName),
prjCnt = VALUES(prjCnt),
profLvlSituCode = VALUES(profLvlSituCode),
badSinhonClassifName = VALUES(badSinhonClassifName);
"""

proxies = {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


url = "https://gs.sac.net.cn/publicity/getSponsorAList"

# 发送请求
response = requests.get(url, proxies=proxies, headers=headers)

def save_data(orderNo,name,orgAbbrName,prjCnt,profLvlSituCode,badSinhonClassifName):
    try:
        cursor.execute(sql,(orderNo,name,orgAbbrName,prjCnt,profLvlSituCode,badSinhonClassifName))
        db.commit()
    except Exception as e:
        logging.error(e)
        db.rollback()


# 检查请求是否成功
if response.status_code == 200:
    try:
        # 解析 JSON 数据
        data = response.json()



        # 检查返回的状态
        if isinstance(data, dict) and data.get('success') and data.get('code') == 20000:
            # 提取关键数据
            sponsor_list = data['data']

            if isinstance(data['data'], dict):
                for sponsor in sponsor_list.items():
                    sponsor_data = sponsor[1]
                    for item in sponsor_data:
                        orderNo = item['orderNo']
                        name = item['name']
                        orgAbbrName = item['orgAbbrName']
                        prjCnt = item['prjCnt']
                        profLvlSituCode= item['profLvlSituCode']
                        badSinhonClassifName = item['badSinhonClassifName']
                        logging.info(f"{orderNo}")
                        save_data(orderNo,name,orgAbbrName,prjCnt,profLvlSituCode,badSinhonClassifName)
                        logging.info("Successfully saved data")

        else:
            print(f"请求失败: {data.get('message', '未知错误')}")
    except requests.exceptions.JSONDecodeError:
        print("响应不是有效的 JSON 格式")
else:
    print(f"请求失败，状态码: {response.status_code}")

db.close()

