from pymavlink import mavutil
import time
import socket
import base64

tcp_ip_sever = "0.0.0.0"
tcp_port_sever= 8000

mavlink_Message = [mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE, mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED, 
                   mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT, mavutil.mavlink.MAVLINK_MSG_ID_RC_CHANNELS, 
                   mavutil.mavlink.MAVLINK_MSG_ID_VFR_HUD, mavutil.mavlink.MAVLINK_MSG_ID_BATTERY_STATUS, 
                   mavutil.mavlink.MAVLINK_MSG_ID_COMMAND_ACK, mavutil.mavlink.MAVLINK_MSG_ID_COMMAND_LONG]
# 30, 32, 33, 65, 74, 147, 77, 11

# sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock_server.connect((tcp_ip_sever, tcp_port_sever))

print("a")
mvk = mavutil.mavlink_connection('tcp:192.168.0.4:5763')
mvk.wait_heartbeat()

def main():
    while(1):
        for request in mavlink_Message:
            mvk.mav.command_long_send(
                mvk.target_system,
                mvk.target_component,
                mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
                0,  # confirmation
                request,
                0, 0, 0, 0, 0, 0  # unused parameters
            )
        
        re = mvk.recv_match(blocking=True)
        if(re.get_type() == 'ATTITUDE'):
            print(re)
        elif(re.get_type() == 'LOCAL_POSITION_NED'):
            print(re)
        elif(re.get_type() == 'GLOBAL_POSITION_INT'):
            print(re)
        elif(re.get_type() == 'RC_CHANNELS'):
            print(re)
        elif(re.get_type() == 'VFR_HUD'):
            print(re)
        elif(re.get_type() == 'BATTERY_STATUS'):
            print(re)    
        print(re)    

if __name__ =="__main__":
    main()