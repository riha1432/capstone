from pymavlink import mavutil
import cv2
import socket
import base64
import time

Re_DataCnt = 20

# 드론 통신 연결
try:
    mavlin = mavutil.mavlink_connection('tcp:192.168.137.1:5763')
    target_system = mavlin.target_system
    target_component = mavlin.target_component
except:
    print("not connected drone")
    # exit()
# mavlin = mavutil.mavlink_connection('COM9', baud=57600)

# 카메라 포트 연결 및 확인
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("not connected camera")
    # exit()

# socket 새팅
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket created")

Mav_Message = []
Dron_data=bytearray(Re_DataCnt)

def int32(x):
    if(x < 0):
        return x | 0X80000000
    else:
        return x
    
def uint8(val, bit):
    return val>>bit & 0X000000FF

def cam_cv2(encode_param):
    ret, frame = cam.read()
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return 0
    if not ret:
        return 0
    ret, buffer = cv2.imencode('.jpg', frame, encode_param)
    if not ret:
        return 0

    data = base64.b64encode(buffer)
    return data
    # s.sendall(data + bytes("끝", 'utf-8'))

def mavlink():
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
        # print(msg)
        if(msg.get_type() == "GLOBAL_POSITION_INT"):
            lat = int32(msg.lat)
            lon = int32(msg.lon)
            alt = msg.alt
            Dron_data[0] = uint8(lat,24)
            Dron_data[1] = uint8(lat,16)
            Dron_data[2] = uint8(lat,8)
            Dron_data[3] = uint8(lat,0)
            Dron_data[4] = uint8(lon,24)
            Dron_data[5] = uint8(lon,16)
            Dron_data[6] = uint8(lon,8)
            Dron_data[7] = uint8(lon,0)
            Dron_data[8] = uint8(alt,8)
            Dron_data[9] = uint8(alt,0)
        elif(msg.get_type() == "BATTERY_STATUS"):
            vol = msg.voltages[0]
            Dron_data[8] = uint8(vol,8)
            Dron_data[9] = uint8(vol,0)
        elif(msg.get_type() == "VFR_HUD"):
            speed = int(msg.groundspeed * 10)
            Dron_data[10] = uint8(speed,8)
            Dron_data[11] = uint8(speed,0)

def setup():
    # 드론 동적 연결상태 확인
    mavlin.wait_heartbeat()
    # 서버 ip, 포트 연결
    try:
        s.connect(('0.0.0.0', 8000))
        print("server connected")
    except:
        print("not connected server")
        # exit()
    
    # 카메라 설정
    cam.set(3, 1280)
    cam.set(4, 480)
    cam.set(cv2.CAP_PROP_FPS, 30)

    # 카메라 연결 확인
    # while True:
    #     if cam.isOpened():
    #         break

    # 드론 요청 데이터
    # Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE) #// 30
    Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED) #// 32
    Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT) #// 33
    Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_RC_CHANNELS) #// 65
    Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_VFR_HUD) #// 74
    Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_BATTERY_STATUS) #// 147

    for i in range(Re_DataCnt):
        Dron_data.append(0)
        
def main():
    # 0~100에서 90의 이미지 품질로 설정 (default = 95)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    while True:
        cam_data = cam_cv2(encode_param)
        # drone_data = mavlink()
        mavlink()
        print(Dron_data)
        Ser_data = cam_data + Dron_data
        print(Ser_data)
        # s.sendall(Ser_data + bytes("끝", 'utf-8'))

    cam.release()
    cv2.destroyAllWindows()
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
