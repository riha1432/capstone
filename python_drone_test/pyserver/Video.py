from ultralytics import YOLO
import base64
from PIL import Image
import numpy as np
import cv2
import io

class Video:
    def __init__(self, model):
        self.AI_model = YOLO(model)
        self.Hcenter = 0
        self.Wcenter = 0
        self.video = None

    def input(self, img):
        # imgdata = img
        imgdata = base64.b64decode(img)
        img_out = Image.open(io.BytesIO(imgdata))
        img_out = np.array(img_out)
        img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)
        video = cv2.resize(img_out, (640, 480))
        return video

    def Object_track(self, video, cmd, socket, data):
        results = self.AI_model.track(video, persist=True, conf = 0.25, verbose = False, vid_stride = 1)
        video = results[0].plot()
        try:
            for i in range(0, len(results[0].boxes.id)):
                if(cmd.id == int(results[0].boxes.id[i])):
                    # print(results[0].boxes.xyxy)
                    cmd.Hcenter = int((results[0].boxes.xyxy[i][1] + results[0].boxes.xyxy[i][3]) / 2)
                    cmd.Wcenter = int((results[0].boxes.xyxy[i][0] + results[0].boxes.xyxy[i][2]) / 2)
                    cmd.mode = 5
                    break
            if(cmd.id == 0):
                cmd.Hcenter = 0
                cmd.Wcenter = 0
                cmd.mode = 0

        except:
            cmd.Hcenter = 0
            cmd.Wcenter = 0
            cmd.mode = 0
            
        socket.Server_Send(data, cmd)
        cv2.imshow('server', video)
        cv2.waitKey(1)