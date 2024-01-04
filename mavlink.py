from pymavlink import mavutil
from pymavlink.dialects.v20 import ardupilotmega
from pymavlink.dialects.v20 import common
import time


# print('hear sys : %u comp : %u'%(mavlin.target_system, mavlin.target_component))

# # land 9
# # hom 6
# mavlin.set_mode_apm(4, 1, 1)

# mavlin.mav.command_long_send(mavlin.target_system, mavlin.target_component, 
#                           common.MAV_CMD_COMPONENT_ARM_DISARM,0, 1,0,0,0,0,0,0)
# msg = mavlin.recv_match(type = 'COMMAND_ACK', blocking=True)
# print(msg)

# time.sleep(2)
# mavlin.mav.command_long_send(mavlin.target_system, mavlin.target_component,
#                               common.MAV_CMD_NAV_TAKEOFF, 0, 0,0,0,0,0,0,10)
# msg = mavlin.recv_match(type = 'COMMAND_ACK', blocking=True)
# print(msg)

# time.sleep(10)
# # mavlink.mav.command_long_send(mavlink.target_system, mavlink.target_component, )
# mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, mavlin.target_system, mavlin.target_component,
#                                                                              mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), 20,0,-10, 0,0,0, 0,0,0, 0,0))
# msg = mavlin.recv_match(type = 'COMMAND_ACK', blocking=True)
# print('1',msg)

# time.sleep(10)
# mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, mavlin.target_system, mavlin.target_component,
#                                                                              mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), -100,0,-15, 0,0,0, 0,0,0, 0,0))

# for _ in range(100):
#     mavl = mavlin.recv_match()
#     print(mavl)
#     time.sleep(1)

# print("home")
# mavlin.set_mode_apm(6, 1, 1)
# time.sleep(20)
# mavlin.set_mode_apm(9, 1, 1)

def main():
    mvk = mavutil.mavlink_connection('tcp:localhost:5763')
    mvk.wait_heartbeat()
    mvk.mav.request_data_stream_send(mvk.target_system, mvk.target_component, mavutil.mavlink.MAV_DATA_STREAM_ALL, 5, 1)

    while(1):
        re = mvk.recv_match()
        print(re)

if __name__ =="__main__":
    main()