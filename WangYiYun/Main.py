import requests
from DrissionPage import ChromiumPage

Base_url = "https://music.163.com/"
USERNAME = 18249555724
PASSWORD = "chqteng1234"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    # 'cookie': 'hb_MA-BE1B-B326EA1BA2C0_source=www.google.com; hb_MA-BFB6-AC673A756684_source=qy.163.com; nts_mail_user=chqteng1234@163.com:-1:1; NTES_P_UTID=USQVcGZUH4jfgVfCKQr6x0zRYZedBVpL|1726054178; MAIL_AGGREGATION_PASSPORT_INFO="chqteng1234@163.com|1726054178|1"; NMTID=00OvYmRKSUbdBysbEtSiMOKB9dNJ1IAAAGSCo-i9A; _iuqxldmzr_=32; _ntes_nnid=205689d7b49edff3737c78d6e65c639f,1726754039277; _ntes_nuid=205689d7b49edff3737c78d6e65c639f; WEVNSM=1.0.0; WNMCID=cdriek.1726754040575.01.0; __snaker__id=d8WuvRZA90KzSNwr; ntes_utid=tid._.CzckzZ75E3NAElFFQRKDXFCM1O%252Ff47rF._.0; sDeviceId=YD-iVfVgf1T6FtBRlUBUFeWSQHckP7O5rvT; WM_NI=nfzN5ZoXM5hqP9K1CdWtRyaJj7lvdJK%2BvUME%2B7H5w0sPI9W1SnWNGLvyJfl%2B%2FbZyzEjtLJBmln1yCtpuk%2FiUHGqWwI7S2kS8e14hQnn3f%2FOIli4WDkbW20qhhdmcz07oeWw%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed7f06aa9f0bca6b57997b08fb2c15b939b9aacd25086899699e13e94abfea7d82af0fea7c3b92aaebab6afb852ad8883d6eb7b94e785d2c27095ac9e9ae442aae9a497e74289f5bab6d04fe9e988d6f63cb19087dad63b91b299afc648b6a78687ef21edbe969af94faaac84abc167b0b2ff9ac280b4aba5d0ec5f8c99bfb8f643f58dfe8cd234a7effc89d466aeedaad0ce43b0b7fcb8c761a289fed1f464acbca384f93cf5b1abb8f637e2a3; WM_TID=EK2e4OJtXIdBVAEEEVKSXAGJ0Pqf7iRR; P_INFO=18249555724|1726754425|1|music|00&99|null&null&null#shh&null#10#0|&0||18249555724; ntes_kaola_ad=1; JSESSIONID-WYYY=MSgQrEvbNcmCYQx4PHSXYhG9pfpepqT4mWV9sFS1gRbhkry7RDND5oIv%5CKNlQhgkHJ5KHMCbV9nlnR%2B5xV%2BHuVHQiIfeUkz9zQDxr0KIZ7kVnRa9k8pd7eAXF8k7M2zRqZ7eR1NG69T7hHFsnRc%2BQ7N1eCtH5FAjYVFzceIhxRTOblRD%3A1726796377153; gdxidpyhxdE=JkB6p%2BhchooGkRvnGX%2FS2W7xbxx%2F%2BOchRPcfXDK%2F9OcS4M5%5C726gI%5C%5CMUkVbIKKOJoLz1O31MosyXqXfb%2FOeNuM%2FpNJiMZJ1P3Nit5llg3sgWTi09hGlJo%5C%2BJVxfJ58sUDyQBD4XOvQuB8oATHO9%2F9d%2B3Xa7uyv5OyGqgGOouRTbmmRp%3A1726795497595; MUSIC_U=00654CC2A7AE2201150C4B2D46E7CCDDCE5525ECE02CA2A73E1D7A9DE7066F2BAD67600CEC560AA53DBE4DA172118E834C063303CE8449F75C67D01E6581DD28BA01EB39208449EA16B95B07D72A2A726B07F8FE75F39A72766707D99F3CFE14E85F9434CDD4B3D220A0B7EB6BCD605E95B99E2AE37DB3B9CEABFAE7AF0BBB87975CBC5B6B573E02D3E85176ABB86C09120AE3F300D772E9FFD9735576B874764C52E6111CCD317D68DE05DFEA385091803E73F10242A77C92602CA6735D441B523BA3B5661F233CCFF324A0CCE3F0936F3D0BC6FCB4B1E09FA46029585AB1A93E2FABE66D80298CDA54B587EB1D069BAF62C7417F9B4F842BCF0D7122EADD3F630C91C050C924D7A91B0370F3C0BA73BBDC2306D38EE5FE13AC4838D9B954B05121B2A0AE7CA19F674BB88B38A8BD76615987AD97A295E4F114D1D8C9A4FEC7D5CF64C7C3AFF9248D1724911466F47D92; __csrf=f02f042b5e253fd7dca7323dedda708a',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://music.163.com/playlist?id=615267582',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

proxies = {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}


def login(USERNAME, PASSWORD):
    page = ChromiumPage()
    page.get(Base_url)
    page.ele("//input[@class=\"_2OT0mQUQ\"]").input(USERNAME)
    page.ele("//input[@class=\"sR89MU1J\"]").input(PASSWORD)
    page.ele("//div[@class=\"tan2MIhq\"]").click()


def main():
    login(USERNAME, PASSWORD)


    main()
