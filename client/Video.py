import cv2
import base64
import numpy as np
import math
from matplotlib import pyplot as plt
from Error import Error

WIDTH = 3
HEIGHT = 4

class Video:
    def __init__(self, quality = 95):
        self.cam = None 
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        self.ret = None
        self.frame = None
        self.imgL = None
        self.imgR = None

    def Connect(self, port):
        self.cam = cv2.VideoCapture(port)
        if not self.cam.isOpened():
            print("dont connect to camera")
            Camera_Check = True
            Error(3)
        else:
            print('connect to camera')
        return
    
    def Close(self):
        self.cam.release()
        cv2.destroyAllWindows()
        return

    def VidoeSetup(self, width, height, frame):
        self.cam.set(3, width)
        self.cam.set(4, height)
        self.cam.set(cv2.CAP_PROP_FPS, frame)
        return

    def __video(self):
        self.ret, self.frame =  self.cam.read()
        if not self.ret:
            return None
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return None
        cv2.imshow('frame',self.frame)
        return
    
    def VideoData(self):
        self.__video()

        ret, buffer = cv2.imencode('.jpg', self.frame, self.encode_param)
        
        if not ret:
            return None
        
        data = base64.b64encode(buffer)
        return data
    
    def Distance(self, x, y):
        self.imgL = cv2.cvtColor(self.frame[ : , :640], cv2.COLOR_BGR2GARY)
        self.imgR = cv2.cvtColor(self.frame[ : , 640:], cv2.COLOR_BGR2GARY)

        stereo = cv2.StereoBM_create(numDisparities=96, blockSize=5)
        disparity = stereo.compute(self.imgL, self.imgR)
        deep = 12
        return deep
    
    def Object_Dis(self, radi, height):
        cos = math.cos(radi)
        cos = height / cos
        sin = math.size(radi) * cos
        return cos, sin


