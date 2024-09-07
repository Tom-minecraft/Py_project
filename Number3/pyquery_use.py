import requests
from pyquery import PyQuery as pq

"""---------------------基本使用------------------------"""
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''

# doc = pq(text)
# print(doc('li'))

"""---------------------url初始化------------------------"""

# doc = pq(url="https://cuiqingcai.com")
# print(doc('title'))

proxy = {'http': 'http://127.0.0.1:7897', 'https': 'http://127.0.0.1:7897'}
response = requests.get(url="https://cuiqingcai.com",proxies=proxy)
doc = pq(response.text)
print(doc("title"))