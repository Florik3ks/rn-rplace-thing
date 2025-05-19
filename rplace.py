import time
from socket import *

from PIL import Image

img = Image.open('sylveon.png')

i = 0
imgdata = list(img.getdata())
def next_pixel():
    global i
    print(i)
    x = i % img.size[0]
    y = i // img.size[1]
    imgd = imgdata[i][:3]

    color = '#%02x%02x%02x' % imgd
    i += 1 
    i %= img.size[0] * img.size[1]
    return x,y,color

base_x = 478
base_y = 360
def get_msg():
    x,y,color = next_pixel()
    x += base_x
    y += base_y
    return f"place {x} {y} {color}\r\n"

client = socket(AF_INET, SOCK_STREAM)
client.settimeout(0.5)

ip = "148.251.181.111"
port = 6666
addr = (ip, port)
while True:
    try:
        client.connect(addr)
        data, server = client.recvfrom(1024, )
        print(data)
        while True:
            msg = get_msg()
            print(msg)
            client.send(msg.encode('utf-8'))
            print(data)
            time.sleep(1)
    except Exception as e:
        print(":(", e)
        time.sleep(2)