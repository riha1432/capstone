import socket
from Error import Error

REQUEST_DATA = 20

class Socket:
    def __init__(self):
        self.socket = None
        self.Server_data = None

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
        self.socket.sendall(video + bytes("_D_",'utf-8') + data + bytes("_E_", 'utf-8'))
        return

    def Receive(self):
        while True:
            print('<<', end=' ')
            self.Server_data = self.socket.recv(20)
            print('>>')
        return