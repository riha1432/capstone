import pickle
import socket
import struct
import base64
from PIL import Image
import io
import cv2
import numpy as np

HOST = 'localhost'
PORT = 8484

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('소켓 생성')

s.bind((HOST, PORT))
s.listen(10)

conn, addr = s.accept()

payload_size = struct.calcsize("L")

while True:
    # while len(data) < payload_size:
    bata = b''
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