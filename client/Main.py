import time
import io
import numpy as np
import Server as Sm
import Drone as Dm
import Video as Vm
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
    Video.VidoeSetup(1280,480,30)
    return
    
def main():
    rq = len(Drone.Mav_Message)
    index = 0
    Drone.Request(index)
    s = time.time()
    th1 = Thread(target=Server.Receive, args=(Cmd))
    th1.start()

    while True:
        num = Drone.Receive(Dron_data, Status)
        if num == index:
            index = (index + 1) % rq
            Drone.Request(index)
        
        video = Video.VideoData()
        Server.Send(video, Dron_data)

        Drone.Sendcommand(Cmd)
        Video.Object_Dis(45 + Status.pitch)


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
