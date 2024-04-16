import time
import io
import numpy as np
import Server as Sm
import Drone as Dm
import Video as Vm

# mavlin = mavutil.mavlink_connection('tcp:localhost:5763')
# mavlin = mavutil.mavlink_connection('COM9', baud=57600)

Server = Sm.Socket()
Drone = Dm.Mavlink()
Video = Vm.Video(90)
Dron_data=bytearray(Sm.REQUEST_DATA)
Server_data=bytearray(Sm.REQUEST_DATA)

def setup():
    Server.Connect('localhost', 8000)
    Drone.Connect('tcp:localhost:5763')
    # Drone.Connect('COM9', 57600)
    Video.Connect(0)
    Video.VidoeSetup(1280,480,30)
    return
    
def main():
    while True:
        Drone.Request()
        Drone.Receive()

        video = Video.VideoData()
        Server.Send(video, Dron_data)

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
