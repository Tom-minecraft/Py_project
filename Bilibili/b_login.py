import requests
from pprint import pprint
import execjs
node = execjs.get()

with open("./b_decode.js" , "r" , encoding='utf-8') as f:
    ctx = execjs.compile(f.read())

password = ctx.call("RSA_Public_Encrypt","chqteng1234")
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': "buvid3=C0BC092F-D133-5528-5BFF-978E18482AB419732infoc; b_nut=1723465719; _uuid=462C8B3B-F1094-CDF2-1D710-10AD10ACB6849E19952infoc; enable_web_push=DISABLE; buvid4=3F2889D1-F8C8-3EEA-227C-5630D669042B21116-024081212-QxSPvbGViySsvEkYlWJKjA%3D%3D; rpdid=|(k|Yl~k)J0J'u~kJRYl)Ju; header_theme_version=CLOSE; buvid_fp_plain=undefined; home_feed_column=5; fingerprint=7f2e05100f57c815cdb15b14616f58e6; CURRENT_QUALITY=0; LIVE_BUVID=AUTO6817263323909268; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjcxNzExNzMsImlhdCI6MTcyNjkxMTkxMywicGx0IjotMX0.ax5rBpMVBZxM707nrVysZQwM_UYduJZzCovdOfkkF1w; bili_ticket_expires=1727171113; buvid_fp=7f2e05100f57c815cdb15b14616f58e6; is-2022-channel=1; b_lsid=101110BBBB_1921DB24DF3; sid=6vklbhao; bp_t_offset_457045006=980279049261678592; browser_resolution=1536-418",
    'origin': 'https://www.bilibili.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.bilibili.com/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

data = {
    'username': '18249555724',
    'password': password,
}

proxies = {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}


response = requests.post('https://passport.bilibili.com/x/passport-login/web/login',  headers=headers, data=data , proxies= proxies)
cookies = response.cookies
session = requests.session()
for name, value in cookies.items():
    session.cookies.set(name, value)

res = session.get('https://www.bilibili.com/',headers=headers , proxies=proxies)
pprint(res.text)