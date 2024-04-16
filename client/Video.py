import cv2
import base64
import numpy as np
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

    def Connect(self, port):
        self.cam = cv2.VideoCapture(port)
        if not self.cam.isOpened():
            print("dont connect to camera")
            Camera_Check = True
        else:
            Error(3)
        return
    
    def Close(self):
        self.cam.release()
        cv2.destroyAllWindows()
        return

    def VidoeSetup(self, width, height, frame):
        self.set(WIDTH, width)
        self.set(HEIGHT, height)
        self.set(cv2.CAP_PROP_FPS, frame)
        return

    def __video(self):
        self.ret, self.frame =  self.cam.read()
        if not self.ret:
            return None
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return None
        return
    
    def VideoData(self):
        self.__video()

        ret, buffer = cv2.imencode('.jpg', self.frame, self.encode_param)
        
        if not ret:
            return None
        
        data = base64.b64encode(buffer)
        return data
    
    def Distance(self, x, y):
        imgL = []
        imgR = []
        stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
        disparity = stereo.compute(imgL, imgR)
        deep = 12
        return deep


