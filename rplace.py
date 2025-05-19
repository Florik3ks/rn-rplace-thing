import time
import random
from socket import *
import traceback
from colorama import Fore, Style

from PIL import Image

img = Image.open('img/mrow.png')
startx = 456
starty = 350

pixels = {}


def prep_img():
    imgdata = list(img.getdata())
    for y_ in range(img.height):
        for x_ in range(img.width):
            x = startx + x_
            y = starty + y_
            i = x_ + y_ * img.width
            if imgdata[i][3] == 0:
                continue
            imgd = imgdata[i][:3]

            color = '#%02x%02x%02x' % imgd
            pixels[(x, y)] = color


i = 0
prep_img()
keys = list(pixels.keys())
random.shuffle(keys)


def next_pixel(client):
    global i
    while True:
        for _ in range(95):
            (px, py) = keys[i]
            color = pixels[keys[i]]
            client.send(f"get {px} {py}\r\n".encode('utf-8'))
            data, server = client.recvfrom(1024, )
            current = data.decode("utf-8").split("#")[1][:6]
            i += 1
            i %= img.width * img.height
            if color != f"#{current}":
                return px, py, color
            else:
                print(f"{Style.DIM}skip {px}, {py}{Style.RESET_ALL}")
        time.sleep(1)


def get_msg(client):
    x, y, color = next_pixel(client)
    return f"place {x} {y} {color}\r\n"


ip = "148.251.181.111"
port = 6666
addr = (ip, port)

while True:
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.settimeout(0.5)

        client.connect(addr)
        data, server = client.recvfrom(1024, )
        print(data)
        while True:
            msg = get_msg(client)
            print(msg.strip())
            client.send(msg.encode('utf-8'))
            data, server = client.recvfrom(1024, )
            print(Fore.LIGHTMAGENTA_EX, data.decode("utf-8").strip(), Style.RESET_ALL, sep='')
            time.sleep(1)
    except TimeoutError:
        print("timeout :(")
    except Exception as e:
        print(":(", e)
        print(traceback.format_exc())
        time.sleep(2)
