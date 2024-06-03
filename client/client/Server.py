import socket
from Error import Error
import time

REQUEST_DATA = 20

class Socket:
    def __init__(self):
        self.socket = None
        self.Server_data = None

    def __uint7(self, val, bit):
        return val<<bit
    
    def Connect(self, ip, port): 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.socket.connect((ip, port))
                print("connect to server")
                break
            except:
                pass
        return
    
    def Close(self):
        self.socket.close()
        return

    def Send(self, video, data):
        self.socket.sendall(video + bytes("_D_",'utf-8') + data + bytes("_E_", 'utf-8'))
        # print(len(video) + len(data))
        return

    def Receive(self, Cmd, Drone):
        print('thread')
        while True:
            self.Server_data = self.socket.recv(20)
            # print(self.Server_data)
            Cmd.videoObjectCenterH = self.__uint7(self.Server_data[0], 7) | self.Server_data[1]
            Cmd.videoObjectCenterW = self.__uint7(self.Server_data[2], 7) | self.Server_data[3]
            Cmd.CommendLat = ( self.__uint7(self.Server_data[4], 28) | self.__uint7(self.Server_data[5], 21) | 
                            self.__uint7(self.Server_data[6], 14) | self.__uint7(self.Server_data[7], 7) | self.Server_data[8] )
            Cmd.CommendLon = ( self.__uint7(self.Server_data[9], 28) | self.__uint7(self.Server_data[10], 21) | 
                            self.__uint7(self.Server_data[11], 14) | self.__uint7(self.Server_data[12], 7) | self.Server_data[13] )
            # Cmd.Height = self.__uint7(self.Server_data[14], 7) | self.Server_data[15]
            Cmd.Commend = self.Server_data[14]
            Drone.SetMode(Cmd)
        return