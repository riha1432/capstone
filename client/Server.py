import socket
from Error import Error

REQUEST_DATA = 20

class Socket:
    def __init__(self):
        self.socket = None

    def Connect(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((ip, port))
            print("connect to server")
        except:
            Error(1)
        return
    
    def Close(self):
        self.socket.close()
        return

    def Send(self, video, data):
        # self.socket.sendall(video + bytes("끝",'utf-8') + data + bytes("끝", 'utf-8'))
        self.socket.sendall(video + bytes("끝",'utf-8'))
        return

    def Receive(self, data):
        return