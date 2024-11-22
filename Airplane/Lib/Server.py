import socket
import asyncio
import ray
import numpy as np

import Lib.Commend as CMD
import Lib.uint as UINT

@ray.remote
class SERVER:
    def __init__(self):
        self.socket: socket = None
        self.rece_data: list[] = []
        self.cmd: CMD.Commend = CMD.Commend()

    def connect(self, address, port) -> bool:
        print("========Server connecting========")
        while True:
            try:
                self.sockeet.connect((address, port))
                print("       Server connection complete       ")
                return 1
            except:
                pass

        return 0

    def close(self):
        self.socket.close()

    def transmit(self, video: np.ndarray, data:  np.ndarray) -> bool:
        try:
            self.socket.sendall(video + bytes("_D_",'utf-8') + data + bytes("_E_", 'utf-8'))
            return 1
        except:
            print("transmission failed")
            return 0

    def Receive(self) -> CMD.Commend:

        self.Server_data = self.socket.recv(20)
        self.cmd.videoObjectCenterH = UINT.uint7(self.Server_data[0], 7) | self.Server_data[1]
        self.cmd.videoObjectCenterW = UINT.uint7(self.Server_data[2], 7) | self.Server_data[3]
        self.cmd.CommendLat = ( UINT.uint7(self.Server_data[4], 28) | UINT.uint7(self.Server_data[5], 21) | 
                        UINT.uint7(self.Server_data[6], 14) | UINT.uint7(self.Server_data[7], 7) | self.Server_data[8] )
        self.cmd.CommendLon = ( UINT.uint7(self.Server_data[9], 28) | UINT.uint7(self.Server_data[10], 21) | 
                        UINT.uint7(self.Server_data[11], 14) | UINT.uint7(self.Server_data[12], 7) | self.Server_data[13] )
        # self.cmd.Height = UINT.uint7(self.Server_data[14], 7) | self.Server_data[15]
        self.cmd.Commend = self.Server_data[16]
        
        return self.cmd

    