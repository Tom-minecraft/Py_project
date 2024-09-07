import pymongo
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

Mongo_connection_string = 'mongodb://localhost:27017/'
Mongo_db = "Movies"
Mongo_collection = "movies"

client = pymongo.MongoClient(Mongo_connection_string)
db = client[Mongo_db]
collection = db[Mongo_collection]




def scrape_api(url):
    logging.info("Scraping %s ..." ,url)
    try:
        response = requests.get(url, proxies=proxies)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error("Status_code: %s ", response.status_code)
            return {}

    except requests.RequestException as e:
        logging.error("Something wrong:", exc_info=True)

def scrape_index(page):
    url = index_url.format(limit=per_page, offset=(page-1)*per_page)
    return scrape_api(url)

def scrape_detail(id):
    url = detail_url.format(id=id)
    return scrape_api(url)

def save_data(data):
    collection.update_one({'name':data.get('name')}, {'$set':data}, upsert=True)

def main():
    try:
        for page in range(1, total_pages+1):
            index_data = scrape_index(page)
            for item in index_data["results"]:
                id = item.get("id")
                detail_data = scrape_detail(id)
                logging.info('Detail_data got : %s', detail_data)
                save_data(detail_data)
                logging.info('Data saved successfully')
    finally:
        client.close()



if __name__ == '__main__':
    main()


