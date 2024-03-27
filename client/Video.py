import cv2
import base64
from Error import Error

WIDTH = 3
HEIGHT = 4

class Video:
    def __init__(self, quality = 95):
        self.cam = None 
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]

    def Connect(self, port):
        self.cam = cv2.VideoCapture(port)
        if self.cam.isOpened():
            print("connect camera")
        else:
            Error(3)
        return
    
    def Close(self):
        self.cam.release()
        cv2.destroyAllWindows()
        return

    def VidoeSetup(self, width, height, frame):
        self.cam.set(WIDTH, width)
        self.cam.set(HEIGHT, height)
        self.cam.set(cv2.CAP_PROP_FPS, frame)
        return

    def VideoData(self):
        ret, frame = self.cam.read()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return None
        if not ret:
            return None
        
        ret, buffer = cv2.imencode('.jpg', frame, self.encode_param)
        
        if not ret:
            return None
        
        data = base64.b64encode(buffer)

        return data
    
    def Distance(self):
        return


