from pymavlink import mavutil
from pymavlink.dialects.v20 import common
import time
import inspect
# 드론 연결 정보 설정
mavlin = mavutil.mavlink_connection('tcp:localhost:5763')

# mavlin = mavutil.mavlink_connection('COM7', baud=57600)

# 메시지 수신 대기 시작
mavlin.wait_heartbeat()

mavlin.arducopter_arm()
time.sleep(1)
mavlin.set_mode_apm(13, 1, 1)

time.sleep(5)

mavlin.set_mode_apm(15, 1, 1)

time.sleep(3)

mavlin.mav.mission_item_int_send(
    mavlin.target_system,  # target_system
    mavlin.target_component,  # target_component
    0,  # seq
    mavutil.mavlink.MAV_FRAME_GLOBAL_TERRAIN_ALT_INT,  # frame
    17,  # command
    2,  # current
    0,  # autocontinue
    0,  # param1
    0,  # param2
    0,  # param3
    0,  # param4
    -353621474,  # x (int32)
    1491300000,  # y (int32)
    100)

# # ARM 명령 전송
# mavlin.mav.command_long_send(mavlin.target_system, mavlin.target_component, 
#                           common.MAV_CMD_COMPONENT_ARM_DISARM,0, 1,0,0,0,0,0,0)

# time.sleep(5)

# # # TAKEOFF 명령 전송
# # msg = mavutil.mavlink_command_long_message(mavlin.target_system, mavlin.target_component, 
# #     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0)
# # mavlin.send_message(msg)

# time.sleep(10)
# # mavlin.set_mode_apm(13, 1, 1)

# # mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, mavlin.target_system, mavlin.target_component,
# 
                                                                            #  mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), Send[index].x,Send[index].y,Send[index].z, 0,0,0, 0,0,0, 0,0))
# mavlin.mav.send(common.mavlink_mission_item_int_message(
    # 10,  # seq
    # mavlin.target_system,  # target_system
    # mavlin.target_component,  # target_component
    # mavutil.mavlink.MAV_FRAME_GLOBAL,  # frame
    # common.MAV_CMD_NAV_LOITER_TO_ALT,  # command
    # 1,  # current
    # 1,  # autocontinue
    # 0,  # param1
    # 0,  # param2
    # 0,  # param3
    # 0,  # param4
    # 353621474,  # x (int32)
    # 1400000000,  # y (int32)
    # 700))  # z
                
                
# # GUIDED 모드로 변경
# 0 Manual
# 1 circle
# 2 stabilize
# 3 training
# 4 acro
# 5 fbwa
# 6 fbwb
# 7 cruise
# 8 autotune
# 10 auto
# 11 rtl
# 12 loiter
# 13 takeoff
# 14 avoid_adsb
# 15 guided
# 17 Qstabilize
# 18 Qhober
# 19 Qloiter
# 20 qland
# 21 Qrtl
# 22 Qautotune
# 23 Qacro
# 24 thermal
# 25 loiter to Qland


# 이동 속도 설정
# vx = 1.0 # m/s
# vy = 0.0 # m/s
# vz = 0.0 # m/s

# # 이동 명령 전송
# msg = mavutil.mavlink_set_position_target_local_ned_message(connection.target_system, connection.target_component, 
#     mavutil.mavlink.MAV_FRAME_LOCAL_NED, 0, 0, 0, vx, vy, vz, 0, 0)
# connection.send_message(msg)
