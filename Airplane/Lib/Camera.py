import cv2
import numpy as np
import base64
import math
import asyncio
import ray

@ray.remote
class Camera:
    def __init(self, quality = 90):
        self.cap = None
        self.frame = None
        self.camera_L = None
        self.camera_R = None
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        self.width = 0
        self.height = 0
        self.ret = None
        self.buffer = None

    def connect(self, width :int, height:int, frame: int) -> bool:
        port = 0
        print("========Camera connecting========")
        while True:
            try:
                self.cap = cv2.VideoCapture(port)
                print("       Camera connection complete       ")
                break
            except:
                print(f"error : {port} Not that port")
                port = port + 1
                pass

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cam.set(cv2.CAP_PROP_FPS, frame)

        return 1
    
    def __video(self) -> bool:
        try:
            self.ret, self.frame = self.cap.read()
            if not self.ret:
                return 0
            cv2.waitKey(1)
            return 1
        except:
            print("error : video read error")

    def VideoData(self):
        self.__video()
        try:
            ret, self.buffer = cv2.imencode('.jpg', self.frame, self.encode_param)
            data = base64.b64encode(self.buffer)
            return data
        except:
            print("err")
            return ""
            
