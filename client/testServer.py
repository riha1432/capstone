import pickle
import socket
import struct
import base64
from PIL import Image
import io
import cv2
import numpy as np
from threading import Thread
import sys
import time

HOST = 'localhost'
PORT = 8484
Send = bytearray(20)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('소켓 생성')
s.bind((HOST, PORT))
s.listen(10)
conn, addr = s.accept()

payload_size = struct.calcsize("L")

end = 0

id = -1
mode = 0
pixelH = 0
pixelW = 0

def Object_ID():
    global end, id, mode
    while True:
        print('0종료/1객체 번호/2모드 ( 입력 형식 : x y): ', end = '')
        cmd = input()
        cmd = cmd.split(' ')
        try:
            if(int(cmd[0]) == 0):
                end = 1
                break
            elif(int(cmd[0]) == 1):
                id = int(cmd[1])
            elif(int(cmd[0]) == 2):
                mode = int(cmd[1])
                Send[16] = mode
                conn.send(Send)
        except:
            pass
        print(Send)


th1 = Thread(target=Object_ID, args=()) # 서버 데이터 수신
th1.start() # 서버 데이터 수신

while True:
    bata = b''
    if(end == 1):
        exit()
    while True:
        re = conn.recv(4096)
        if(re.endswith(b'_E_')):
            bata += re
            break
        else:
            bata += re
    

    data = bata.split(b'_D_')
    img = data[0]
    data = data[1]

    imgdata = base64.b64decode(img)
    img_out = Image.open(io.BytesIO(imgdata))
    img_out = np.array(img_out)
    img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)
    a = cv2.resize(img_out, (720, 480))
    cv2.imshow('server', a)
    cv2.waitKey(1)