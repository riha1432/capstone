import numpy as np
from Lib.uint import uint7

class Commend:
    def __init__(self):
        self.mode_num = 0
        self.CommendLat = 0
        self.CommendLon = 0
        self.heigth = 10
        self.videoObjectCenterH = 0
        self.videoObjectCenterW = 0

    def array_to_class(self, array: np.ndarray):
        self.videoObjectCenterH = uint7(array[0], 7) | array[1]
        self.videoObjectCenterW = uint7(array[2], 7) | array[3]
        self.CommendLat = ( uint7(array[4], 28) | uint7(array[5], 21) | 
                        uint7(array[6], 14) | uint7(array[7], 7) | array[8] )
        self.CommendLon = ( uint7(array[9], 28) | uint7(array[10], 21) | 
                        uint7(array[11], 14) | uint7(array[12], 7) | array[13] )
        # self.cmd.Height = uint7(array[14], 7) | array[15]
        self.Commend = array[16]

        return 1