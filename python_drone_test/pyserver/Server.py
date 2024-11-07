import socket

class Server:
    def __init__(self):
        self.Socket = None
        self.conn = None
        self.addr = None
        self.data = b''
        self.img = b''
        self.status = b''
    def __uint7(self, val, bit):
        return val>>bit & 0X0000007F
    
    def Produce(self, host, port, listens):
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.bind((host, port))
        self.Socket.listen(listens)
        self.conn, self.addr = self.Socket.accept()
        print("소캣 생성")

    def Reception(self):
        while True:
            re = self.conn.recv(65536)
            Split = re.split(b'_E_')
            if(len(Split) == 1):
                self.data += Split[0]
            else:
                self.data += Split[0]
                d = self.data.split(b'_D_')
                self.img = d[0]
                self.status = d[1]
                self.data = Split[1]

                return self.img, self.status
            
    def Server_Send(self, data, Cmd):
        data[0] = self.__uint7(int(Cmd.Hcenter), 7)
        data[1] = self.__uint7(int(Cmd.Hcenter), 0)
        data[2] = self.__uint7(int(Cmd.Wcenter), 7)
        data[3] = self.__uint7(int(Cmd.Wcenter), 0)
        data[16] = Cmd.mode
        self.conn.send(data)