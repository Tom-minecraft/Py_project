# Target : https://srr1.scrape.center

import requests
from pyquery import PyQuery as pq
import re
proxies = {
    "http": "http://127.0.0.1:7897",
    "https": "http://127.0.0.1:7897"
}

url = 'https://ssr1.scrape.center/'
html = requests.get(url,proxies=proxies)
doc = pq(html.text)
items = doc('.el-card').items()

with open('movies.txt', 'w', encoding='utf-8') as f:
    for item in items:
        # 电影名称
        name = item.find('a > h2').text()
        f.write(f'名称: {name}\n')
        # 类别
        categories = [item.text() for item in item.find('.categories button span').items()]
        f.write(f'类别: {categories}\n')
        # 上映时间
        published_at = item.find('.info:contains(上映)').text()
        published_at = re.search('(\d{4}-\d{2}-\d{2})', published_at).group(1) \
            if published_at and re.search('\d{4}-\d{2}-\d{2}', published_at) else None
        f.write(f'上映时间: {published_at}\n')
        # 评分
        score = item.find('p.score').text()
        f.write(f'评分: {score}\n')
        f.write(f'{"=" * 50}\n')
    