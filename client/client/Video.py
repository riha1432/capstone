import cv2
import base64
import numpy as np
import math
# from matplotlib import pyplot as plt
from Error import Error

WIDTH = 3
HEIGHT = 4
camAngle = 45
WANAGLE_VIEW = 72
HANAGLE_VIEW = 42

class Video:
    def __init__(self, quality = 95):
        self.cam = None 
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        self.ret = None
        self.frame = None
        self.imgL = None
        self.imgR = None
        self.MaxH = 0
        self.MaxW = 0

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
        self.MaxH = height
        self.MaxW = width
        self.cam.set(3, width)
        self.cam.set(4, height)
        self.cam.set(cv2.CAP_PROP_FPS, frame)
        return

    def __video(self):
        self.ret, self.frame =  self.cam.read()
        # if not self.ret:
        #     return None
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     return None
        # cv2.imshow('frame',self.frame)
        return
    
    def VideoData(self):
        self.__video()

        ret, buffer = cv2.imencode('.jpg', self.frame, self.encode_param)
        
        if not ret:
            return None

        data = base64.b64encode(buffer)
        # cv2.imshow('a', buffer)
        # cv2.imwrite('./output.png', img_out)
        return data
    
    # def Stereo(self, x, y):
    #     self.imgL = cv2.cvtColor(self.frame[ : , :640], cv2.COLOR_BGR2GARY)
    #     self.imgR = cv2.cvtColor(self.frame[ : , 640:], cv2.COLOR_BGR2GARY)

    #     stereo = cv2.StereoBM_create(numDisparities=96, blockSize=5)
    #     disparity = stereo.compute(self.imgL, self.imgR)
    #     deep = 12
    #     return deep
    
    def Object_Dis(self, status ,cmd):
        pixelAngleH = (HANAGLE_VIEW / self.MaxH)
        videoHC = (self.MaxH / 2) + (status.Pitch / pixelAngleH)
        pixelAngleH = (videoHC - cmd.videoObjectCenterH) * pixelAngleH
        # print('videoHC : ', videoHC , 'pixelAngleH : ', pixelAngleH, 'cmd.videoObjectCenterH : ',cmd.videoObjectCenterH)

        Cos_Distance = math.cos(math.pi * ((camAngle + pixelAngleH) / 180))
        Cos_Distance = status.Alt / Cos_Distance

        pixelAngleW = (WANAGLE_VIEW / self.MaxW)
        pixelAngleW = (cmd.videoObjectCenterW - (640 / 2)) * pixelAngleW
        Object_Distance = math.cos(math.pi * (pixelAngleW / 180))
        Object_Distance = Cos_Distance / Object_Distance # 객채 거리
        
        Horizontal_Distance = math.sin(math.pi * ((camAngle + pixelAngleH) / 180)) * Object_Distance # 객채 수평 겨리        print("cccc : ",Horizontal_Distance)

        Angle = ( status.Yaw + pixelAngleW )
        
        dNorth = math.cos(math.pi * (Angle / 180))
        dNorth = dNorth * Horizontal_Distance
        dEast = math.sin(math.pi * (Angle / 180))
        dEast = dEast * Horizontal_Distance
        # print(Angle)
        if(Angle < 0):
            Angle = 360 + Angle

        return [dNorth, dEast, Object_Distance, Horizontal_Distance, pixelAngleH, pixelAngleW, Angle]
    
    def Global_Gps_cam45(self, status):
        Cos_Distance = math.cos(math.pi * (45 / 180))
        Cos_Distance = status.Alt / Cos_Distance
        Horizontal_Distance = math.sin(math.pi * (45 / 180)) * Cos_Distance

        dNorth = math.cos(math.pi * (status.Yaw / 180))
        dNorth = dNorth * Horizontal_Distance
        dEast = math.sin(math.pi * (status.Yaw / 180))
        dEast = dEast * Horizontal_Distance

        return [dNorth, dEast]

