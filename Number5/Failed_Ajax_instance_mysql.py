import pymysql
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s  - %(levelname)s - %(message)s')

URL = 'https://spa1.scrape.center/'
per_page = 10
total_pages = 10
index_url = 'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'
detail_url = 'https://spa1.scrape.center/api/movie/{id}'

proxy = '127.0.0.1:7897'
proxies = {
    'http': 'http://' + proxy,
    'https': 'http://' + proxy,
}


def prepare_mysql(cursor):
    try:
        cursor.execute('CREATE DATABASE IF NOT EXISTS MOVIES CHARACTER SET utf8mb4')
        cursor.execute('USE MOVIES')
        make_table = """CREATE TABLE IF NOT EXISTS movies (
                            id INT PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            alias VARCHAR(255),
                            cover VARCHAR(255),
                            category VARCHAR(255),
                            region VARCHAR(255),
                            actor TEXT,
                            director VARCHAR(255),
                            score DECIMAL(3,1),
                            `rank` INT,
                            minute INT,
                            drama TEXT,
                            photos TEXT,
                            published_at VARCHAR(255),
                            updated_at VARCHAR(255)
                        );"""
        cursor.execute(make_table)
    except Exception as e:
        logging.error(f"数据库准备时发生错误: {e}")
        raise  # 抛出异常，以便外部处理


def insert_data(cursor, data):
    table = 'movies'
    keys = ','.join(data.keys())
    values = ','.join(['%s'] * len(data))
    sql = f'INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '
    update = ','.join([f'{key}=%s' for key in data])
    sql += update

    # 确保 data_values 是一个包含值的元组，而不是字典
    data_values = tuple(data.values()) * 2
    try:
        cursor.execute(sql, data_values)
    except Exception as e:
        logging.error(f"插入数据时出错: {e}")
        raise  # 抛出异常，以便外部处理


def scrape_api(url):
    logging.info(f"正在抓取 {url} ...")
    try:
        response = requests.get(url, proxies=proxies)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"响应状态码错误: {response.status_code}")
            return {}
    except requests.RequestException as e:
        logging.error("请求时出错:", exc_info=True)
        return {}


def scrape_index(page):
    url = index_url.format(limit=per_page, offset=(page - 1) * per_page)
    return scrape_api(url)


def scrape_detail(id):
    url = detail_url.format(id=id)
    return scrape_api(url)


def main():
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='chqteng1234')
    cursor = db.cursor()
    try:
        prepare_mysql(cursor)
        for page in range(1, total_pages + 1):
            index_data = scrape_index(page)
            if index_data and "results" in index_data:
                for item in index_data["results"]:
                    id = item.get("id")
                    detail_data = scrape_detail(id)
                    logging.info(f"获取到的详细数据: {detail_data}")
                    if detail_data:
                        insert_data(cursor, detail_data)
        db.commit()  # 提交所有更改
    except Exception as e:
        logging.error(f"发生错误: {e}")
        db.rollback()  # 如果发生错误则回滚
    finally:
        db.close()  # 确保在结束时关闭数据库连接


if __name__ == '__main__':
    main()
