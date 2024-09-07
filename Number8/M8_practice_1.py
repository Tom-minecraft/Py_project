import re
import time
from io import BytesIO

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import numpy as np
import tesserocr
from PIL import Image
from retrying import retry
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def preprocess(image):
    image_process = image.convert('L')
    array = np.array(image_process)
    threshold = 50
    array = np.where(array > threshold, 255, 0)
    image_process = Image.fromarray(array.astype('uint8'))
    return image_process

@retry(stop_max_attempt_number=10, retry_on_result= lambda x : x is False)
def login():
    browser.get('https://captcha7.scrape.center/')
    browser.find_element(By.XPATH, '//input[@type="text"][1]').send_keys('admin')
    browser.find_element(By.XPATH, '//input[@type="password"]').send_keys('admin')
    captcha = browser.find_element(By.CSS_SELECTOR,'#captcha')
    image = Image.open(BytesIO(captcha.screenshot_as_png))
    image_result = preprocess(image)
    captcha_result = tesserocr.image_to_text(image_result)
    captcha_result = re.sub('[^A-Za-z0-9]', '', captcha_result)
    browser.find_element(By.CSS_SELECTOR, '.captcha input[type=text]').send_keys(captcha_result)
    browser.find_element(By.XPATH, '//button[@type="button"]').click()
    try:
        WebDriverWait(browser,5).until(EC.presence_of_element_located((By.XPATH, '//h2[contains(.,"successfully login")]')))
        time.sleep(5)
        browser.close()
        return True
    except TimeoutException:
        return False

if __name__ == '__main__':
    browser = webdriver.Chrome()
    login()