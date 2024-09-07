from selenium import webdriver

proxy = '127.0.0.1:7897'
options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=http://{}'.format(proxy))
browser = webdriver.Chrome(options=options)
browser.get('http://www.httpbin.org/get')
print(browser.page_source)
browser.close()