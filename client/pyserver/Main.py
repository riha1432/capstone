from threading import Thread
import CmdInput
import Server
import Video

FRAMECHECK = 8
frame = 0

Send = bytearray(20)

socket = Server.Server()
Cmd = CmdInput.cmd()
video = Video.Video("yolov8n.pt")


socket.Produce('0.0.0.0', 8484, 10)
def Object_ID():
    while True:
        print('0종료/1객체 번호/2모드 ( 입력 형식 : x y): ', end = '')
        cmd = input()
        cmd = cmd.split(' ')

        try:
            if(int(cmd[0]) == 0):
                exit()
            elif(int(cmd[0]) == 1):
                Cmd.id = int(cmd[1])
            elif(int(cmd[0]) == 2):
                Cmd.mode = int(cmd[1])
                Send[16] = Cmd.mode
                socket.conn.send(Send)
        except:
            print('err')
        print(Send)

th1 = Thread(target=Object_ID, args=()) # 서버 데이터 수신
th1.start() # 서버 데이터 수신

while True:
    img, status = socket.Reception()
    if(frame >= FRAMECHECK):
        frame = 0
        video_data = video.input(img)
        video.Object_track(video_data, Cmd, socket, Send)
        # socket.Server_Send(Send, Cmd)
    frame += 1