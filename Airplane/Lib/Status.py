import numpy as np
from Lib.uint import uint7

class Status:
    def __init__(self):
        self.Roll = 0
        self.Pitch = 0
        self.Yaw = 0
        self.Bettery = 0
        self.NowLon = 0
        self.NowLat = 0
        self.Alt = 0
        self.speed = 0
        self.Data = [reset for reset in range(20)]

    def class_to_array(self) -> np.ndarray:
        send = int(self.NowLat * 10000000)
        self.Data[0] = uint7(send, 28)
        self.Data[1] = uint7(send ,21)
        self.Data[2] = uint7(send, 14)
        self.Data[3] = uint7(send, 7)
        self.Data[4] = uint7(send, 0)

        send = int(self.NowLon * 10000000)
        self.Data[5] = uint7(send, 28)
        self.Data[6] = uint7(send, 21)
        self.Data[7] = uint7(send, 14)
        self.Data[8] = uint7(send, 7)
        self.Data[9] = uint7(send, 0)
        self.Data[10] = uint7(self.Alt, 7)
        self.Data[11] = uint7(self.Alt, 0)
        self.Data[14] = uint7(self.speed,7)
        self.Data[15] = uint7(self.speed,0)
        self.Data[12] = uint7(self.Bettery,7)
        self.Data[13] = uint7(self.Bettery,0)

        return np.array(self.Data)
