import time
import io
import numpy as np
import Server as Sm
import Drone as Dm
import Video as Vm
import Convert as Cv
from threading import Thread

Server = Sm.Socket()
Drone = Dm.Mavlink()
Status = Dm.Status()
Cmd = Dm.Commend()
Video = Vm.Video(90)
Dron_data=bytearray(Sm.REQUEST_DATA)
Server_data=bytearray(Sm.REQUEST_DATA)

ANGLE_VIEW = 54
def setup():
    Server.Connect('localhost', 8484)
    Drone.Connect('tcp:localhost:5763')
    # Drone.Connect('COM9', 57600)
    Video.Connect(0)
    Video.VidoeSetup(640,480,30)
    return
    
def main():
    rq = len(Drone.Mav_Message)
    index = 0
    Drone.Request(index)
    droneSend = s = time.time()

    th1 = Thread(target=Server.Receive, args=(Cmd,)) # 서버 데이터 수신
    th1.start() # 서버 데이터 수신

    O_LastGps = None
    movegps = [0, 0]
    while True:
        Distance = Video.Object_Dis(Status, Cmd) # 거리측정
        O_newgps = Cv.get_location_metres(Status, Distance) # 객채 gps 좌표값
        
        # movegps[0] = (O_LastGps[0] - O_newgps[0]) + Status.NowLat
        # movegps[1] = (O_LastGps[1] - O_newgps[1]) + Status.NowLon

        num = Drone.Receive(Dron_data, Status) # 드론 데이터 수신
        if num == index:
            index = (index + 1) % rq
            Drone.Request(index) # 드론 데이터 요청
        if(time.time() - droneSend > 0.2):
            Drone.Sendcommand(Cmd, Status, Distance[6], movegps) # 드론 데이터 전송
            droneSend = time.time()
            O_LastGps = O_newgps
    
        video = Video.VideoData() # 비디오 수신

        Server.Send(video, Dron_data) # 서버 전송
    
    Server.Close()
    Video.Close()
    return

if __name__ == '__main__':
    setup()
    main()



# # land 9
# # hom 6
# mavlin.set_mode_apm(4, 1, 1)
# print('mode')
# time.sleep(3)


# mavlin.mav.command_long_send(mavlin.target_system, mavlin.target_component, 
#                           common.MAV_CMD_COMPONENT_ARM_DISARM,0, 1,0,0,0,0,0,0)
# print('arm')
# time.sleep(3)

# mavlin.mav.command_long_send(mavlin.target_system, mavlin.target_component,
#                               common.MAV_CMD_NAV_TAKEOFF, 0, 0,0,0,0,0,0,10)
# print('takeoff')
# time.sleep(8)

# mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, mavlin.target_system, mavlin.target_component,
#                                                                              mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), Send[0].x,Send[0].y,Send[0].z, 0,0,0, 0,0,0, 0,0))
