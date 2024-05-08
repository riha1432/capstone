from pymavlink import mavutil
from pymavlink.dialects.v20 import common
import time

mavlin = mavutil.mavlink_connection('tcp:localhost:5763')

target_system = mavlin.target_system
target_component = mavlin.target_component

mavlin.wait_heartbeat()

Mav_Message = []

Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED) #// 32
Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT) #// 33
Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE ) #// 65
Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_VFR_HUD) #// 74
Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_BATTERY_STATUS) #// 147


while(True):
    for message in Mav_Message[1:2]:
        mavlin.mav.command_long_send(
        mavlin.target_system,
        mavlin.target_component,
        mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
        0,  # confirmation
        message,
        0, 0, 0, 0, 0, 0  # unused parameters
    )
    msg = mavlin.recv_match()
    lat = 0
    lon = 0
    if(msg != None):
        if(msg.get_type() == "GLOBAL_POSITION_INT"):
            lat = msg.lat
            lon = msg.lon
            # print(msg)

            mavlin.mav.command_long_send(
                target_system,
                target_component,
                common.MAV_CMD_CONDITION_YAW,
                0,  # confirmation
                90, 0, 0, 0, 0, 0, 0  # unused parameters
            )
            
            # mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, target_system, target_component,
            #                                                                     mavutil.mavlink.MAV_FRAME_GLOBAL_TERRAIN_ALT_INT, int(0b110111111000), -353624074 + 10, 1491627612 + 10, 20, 0.5,0.5,0, 0,0,0, 0,0))
            break
# mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, target_system, target_component,
#                                                                                 mavutil.mavlink.MAV_FRAME_GLOBAL_TERRAIN_ALT_INT, int(0b110111000111), lat + 100, lon + 100, 20, 0,0,0, 0,0,0, 0,0))