from pymavlink import mavutil
from pymavlink.dialects.v20 import ardupilotmega
from pymavlink.dialects.v20 import common
import time
import inspect
print(inspect.getfile(mavutil))
mavlin = mavutil.mavlink_connection('tcp:localhost:5763')
# mavlin = mavutil.mavlink_connection('COM9', baud=57600)

# mav_com = common.MAVLink()
mavlin.wait_heartbeat()
# mavlin.mav.request_data_stream_send(mavlin.target_system, mavlin.target_component,
#                                         mavutil.mavlink.MAV_DATA_STREAM_ALL, 5, 1)
message_id = mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE 

# print('hear sys : %u comp : %u'%(mavlin.target_system, mavlin.target_component))

# # land 9
# # hom 6
mavlin.set_mode_apm(4, 1, 1)
print('mode')
time.sleep(3)

mavlin.mav.command_long_send(mavlin.target_system, mavlin.target_component, 
                          common.MAV_CMD_COMPONENT_ARM_DISARM,0, 1,0,0,0,0,0,0)
print('arm')
time.sleep(3)

mavlin.mav.command_long_send(mavlin.target_system, mavlin.target_component,
                              common.MAV_CMD_NAV_TAKEOFF, 0, 0,0,0,0,0,0,10)
print('takeoff')
time.sleep(8)
# # msg = mavlin.recv_match(type = 'COMMAND_ACK', blocking=True)
# print(msg)

# time.sleep(2)
# mavlin.mav.command_long_send(mavlin.target_system, mavlin.target_component,
#                               common.MAV_CMD_NAV_TAKEOFF, 0, 0,0,0,0,0,0,10)
# msg = mavlin.recv_match(type = 'COMMAND_ACK', blocking=True)
# print(msg)

# time.sleep(10)
# mavlin.mav.command_long_send(mavlin.target_system, mavlin.target_component, )
# mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, mavlin.target_system, mavlin.target_component,
#                                                                              mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), 20,0,-20, 0,0,0, 0,0,0, 0,0))
# print("2")
# msg = mavlin.recv_match(type = 'MISSION_ACK', blocking=True)
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

class Postion:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

Send = []
Send.append(Postion(10,-10,-15))
Send.append(Postion(10,10,-15))
Send.append(Postion(-10,10,-15))
Send.append(Postion(-10,-10,-15))

index = 0
check = 0
mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, mavlin.target_system, mavlin.target_component,
                                                                             mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), Send[0].x,Send[0].y,Send[0].z, 0,0,0, 0,0,0, 0,0))
while(1):
    mavlin.mav.command_long_send(
        mavlin.target_system,
        mavlin.target_component,
        mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
        0,  # confirmation
        mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED,
        0, 0, 0, 0, 0, 0  # unused parameters
    )
    msg = mavlin.recv_match(type='LOCAL_POSITION_NED',blocking=True)
    print(msg)
    # print(msg.x)
    time.sleep(0.5)
    if check == 1 and abs(Send[index].x - msg.x) < 1 and abs(Send[index].y - msg.y) < 1 and abs(Send[index].z - msg.z) < 1:
        check = 0
        index += 1
        if(index > 3):
            break
        mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, mavlin.target_system, mavlin.target_component,
                                                                             mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), Send[index].x,Send[index].y,Send[index].z, 0,0,0, 0,0,0, 0,0))
        print(index)
    else:
        check = 1 
 
time.sleep(3)
# # land 9
# # hom 6
mavlin.set_mode_apm(6, 1, 1)
print('home')

while True:
    mavlin.mav.command_long_send(
        mavlin.target_system,
        mavlin.target_component,
        mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
        0,  # confirmation
        mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED,
        0, 0, 0, 0, 0, 0  # unused parameters
    )
    msg = mavlin.recv_match(type='LOCAL_POSITION_NED',blocking=True)
    print(msg)
    time.sleep(0.5)
    if abs(0 - msg.x) < 1 and abs(0 - msg.y) < 1:
        break

mavlin.set_mode_apm(9, 1, 1)
print('home')
