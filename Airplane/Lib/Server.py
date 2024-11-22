import socket
import asyncio
import ray
import numpy as np

import Lib.Commend as CMD

@ray.remote
class SERVER:
    def __init__(self):
        self.socket: socket = None
        self.rece_data: list[] = []

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

    # def transmit(self, video: np.ndarray, data:  np.ndarray) -> bool:
    def transmit(self, Send_Data: np.ndarray) -> bool:
        try:
            self.socket.sendall(Send_Data)
            # self.socket.sendall(video + bytes("_D_",'utf-8') + data + bytes("_E_", 'utf-8'))
            return 1
        except:
            print("transmission failed")
            return 0

    def Receive(self) -> list:
        self.Server_data = self.socket.recv(20)
        # 
        return self.Server_data

        
        

    