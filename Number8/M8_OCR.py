# BASE_URL = 'http://captcha7.scrape.center/'
import tesserocr
from PIL import Image
import numpy as np
# image_1 = Image.open('pics/captcha_1.png')
# result_1 = tesserocr.image_to_text(image_1)
# print(result_1)
#
# image_2 = Image.open('pics/captcha_2.png')
# result_2 = tesserocr.image_to_text(image_2)
# print(result_2)

"-----------------function-------------------"
def image_to_text(image_path):
    image_process = Image.open(image_path)
    image_process = image_process.convert('L')
    threshold = 120
    array = np.array(image_process)
    array = np.where(array > threshold, 255, 0)
    image_process = Image.fromarray(array.astype('uint8'))
    image_process.show()
    image_result = tesserocr.image_to_text(image_process)
    return image_result

def index_pic(index):
    pic_path = f"pics/captcha_{index}.png"
    return image_to_text(pic_path)

if __name__ == '__main__':
    for i in range(4,7):
        print(index_pic(i))