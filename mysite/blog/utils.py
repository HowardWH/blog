import hashlib
import hmac

import random
import string
from PIL import Image,ImageDraw,ImageFont,ImageFilter

def hashByMD5(value, salt=None):
    md5 = hashlib.md5(value.encode("utf-8"))
    # 盐值
    if salt is not None:
        md5.update(salt.encode("utf-8"))
    return md5.hexdigest()


def hamcByMD5(value, salt):
    md5 = hmac.new(value.encode("utf-8"), salt.encode("utf-8"), "MD5")
    return md5.hexdigest()

#count表示验证码位数
def getString(count=5):
    ran = string.ascii_lowercase + string.ascii_uppercase + string.digits
    char = ""

    for i in range(count):
        char += random.choice(ran)
    return char

#随机颜色生成
def getRandomColor():
    return (random.randint(150,255), random.randint(150,255), random.randint(150,255))



def create_code():
    img = Image.new('RGB', (200,40),(23,23,23))

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype('arial.ttf',27)

    code = getString()

    for t in range(5):
        draw.text((40*t+5,0), code[t], getRandomColor(), font)

    for _ in range(random.randint(0,50)):
        draw.point((random.randint(0,200), random.randint(0,40)), fill=getRandomColor())

    # img = img.filter(ImageFilter.BLUR)
    # img.save(''.join(code) + '.jpg', 'jpeg')
    return img, code



