import pickle
import socket
import struct
import base64
from PIL import Image
import io
import cv2
import numpy as np
from threading import Thread
from ultralytics import YOLO
import sys
import time

HOST = '0.0.0.0'
PORT = 8484
Send = bytearray(20)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('소켓 생성')
s.bind((HOST, PORT))
s.listen(10)
conn, addr = s.accept()
Yolo_model = YOLO("yolov8n.pt")

payload_size = struct.calcsize("L")

end = 0

id = -1
mode = 0
pixelH = 0
pixelW = 0

videoObjectCenterH = 0
videoObjectCenterW = 0
Commend = 0
CommendLat = 0
CommendLon = 0
heigth = 10

def uint7(val, bit):
        return val>>bit & 0X0000007F

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
                print(id)
            elif(int(cmd[0]) == 2):
                mode = int(cmd[1])
                Send[16] = mode
                conn.send(Send)
        except:
            
            conn.send(Send)
            pass
        print(Send)


th1 = Thread(target=Object_ID, args=()) # 서버 데이터 수신
th1.start() # 서버 데이터 수신

prevate = 0
bata = b''
while True:
    if(end == 1):
        exit()
    re = conn.recv(4096)
    d = re.split(b'_E_')
    if(len(d) == 1):
        bata += d[0]
    else:
        bata += d[0]
        data = bata.split(b'_D_')
        img = data[0]
        data = data[1]
        imgdata = base64.b64decode(img)
        img_out = Image.open(io.BytesIO(imgdata))
        img_out = np.array(img_out)
        img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)
        video = cv2.resize(img_out, (640, 480))

        if(prevate == 4):
            prevate = 0
            results = Yolo_model.track(video, persist=True, conf = 0.4, verbose = False, vid_stride = 1)
            video = results[0].plot()
            try:
                for i in range(0, len(results[0].boxes.id)):
                    if(id == int(results[0].boxes.id[i])):
                        print(results[0].boxes.xyxy)
                        videoObjectCenterH = int((results[0].boxes.xyxy[i][1] + results[0].boxes.xyxy[i][3]) / 2)
                        videoObjectCenterW = int((results[0].boxes.xyxy[i][0] + results[0].boxes.xyxy[i][2]) / 2)
                        Commend = 5
                        break
                
                if(id == 0):
                    videoObjectCenterH = 0
                    videoObjectCenterW = 0
                    Commend = 0
                    
                Send[0] = uint7(int(videoObjectCenterH), 7)
                Send[1] = uint7(int(videoObjectCenterH), 0)
                Send[2] = uint7(int(videoObjectCenterW), 7)
                Send[3] = uint7(int(videoObjectCenterW), 0)
                Send[16] = Commend
                conn.send(Send)
            except:
                videoObjectCenterH = 0
                videoObjectCenterW = 0
                Commend = 0
                Send[0] = 0
                Send[1] = 0
                Send[2] = 0
                Send[3] = 0
                Send[16] = Commend
                conn.send(Send)
                pass

            cv2.imshow('server', video)
            cv2.waitKey(1)

        prevate += 1
        bata = d[1]
        # print(results[0].boxes.xyxy)
        