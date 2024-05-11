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
RANGE = 2.5
def setup():
    Server.Connect('localhost', 8484)
    Drone.Connect('tcp:localhost:5763')
    # Drone.Connect('COM9', 57600)
    Video.Connect(0)
    Video.VidoeSetup(640,480,30)
    return
    
def main():
    droneSend = s = time.time()

    th1 = Thread(target=Server.Receive, args=(Cmd,)) # 서버 데이터 수신
    th1.start() # 서버 데이터 수신

    Distance = [0 for i in range(7)]
    O_newgps = [0, 0]
    O_LastGps = [0, 0]
    movegps = [0, 0]

    while True:
        if(Cmd.videoObjectCenterH != 0 and Cmd.videoObjectCenterW != 0):
            Distance = Video.Object_Dis(Status, Cmd) # 거리측정
            # print('Distance', Distance)
            O_newgps = Cv.get_location_metres(Status, Distance) # 객채 gps 좌표값
            # print('new', O_newgps)
            if(O_LastGps != 0 and O_LastGps != 0):
                movegps[0] = int(((O_LastGps[0] - O_newgps[0]) + (Status.NowLat * 10000000)))
                movegps[1] = int(((O_LastGps[1] - O_newgps[1]) + (Status.NowLon * 10000000)))
            # print('move',movegps)
            # print(Distance[6], (O_LastGps[0] - O_newgps[0]) / 10000000.0, (O_LastGps[1] - O_newgps[1]) / 10000000.0)

        Drone.Receive(Dron_data, Status) # 드론 데이터 수신
        if(time.time() - droneSend > 0.2):
            if(Distance[2] < RANGE and Distance[2] > RANGE and Distance[3] < RANGE and Distance[3] > RANGE):
                pass
            else:
                Drone.Sendcommand(Cmd, Status, Distance, movegps) # 드론 데이터 전송
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
