from pymavlink import mavutil

mavlin = mavutil.mavlink_connection('tcp:192.168.137.1:5763')

target_system = mavlin.target_system
target_component = mavlin.target_component

mavlin.wait_heartbeat()

Mav_Message = []

Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED) #// 32
Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT) #// 33
Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_RC_CHANNELS) #// 65
Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_VFR_HUD) #// 74
Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_BATTERY_STATUS) #// 147

while(True):
    for message in Mav_Message:
        mavlin.mav.command_long_send(
        mavlin.target_system,
        mavlin.target_component,
        mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
        0,  # confirmation
        message,
        0, 0, 0, 0, 0, 0  # unused parameters
    )
    msg = mavlin.recv_match()
    if(msg != None):
        if(msg.get_type()() !="COMMAND_ACK"):
            print(msg)
