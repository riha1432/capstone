from dronekit import connect, VehicleMode, Command, LocationGlobal
from pymavlink import mavutil
from pymavlink.dialects.v20 import common
from Error import Error
import math

OFFSET_X = 10

class Mavlink:
    def __init__(self):
        self.Message_Id = None
        self.Target_System = None
        self.Target_Component = None
        self.mavlin = None
        self.vehicle = None

    def __int32(self, x):
        if(x < 0):
            return x | 0X80000000
        else:
            return x
        
    def __uint7(self, val, bit):
        return val>>bit & 0X0000007F
    
    def Connect(self, address, baud = 0):
        try:
            print("drone connecting .........")
            if(baud == 0):
                self.vehicle = connect(address, wait_ready=True)
                # self.mavlin = mavutil.mavlink_connection(address)
            else:
                self.vehicle = connect(address, baud=baud, wait_ready=True)
                # self.mavlin = mavutil.mavlink_connection(address, baud=baud)
            
            # self.message_id = mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE 
            # self.target_system = self.mavlin.target_system
            # self.target_component = self.mavlin.target_component

        except:
            Error(2)

        return 1

    def Receive(self, Data, status):
        status.Roll = self.vehicle.attitude.roll * (180/math.pi)
        status.Pitch = self.vehicle.attitude.pitch * (180/math.pi)
        status.Yaw = self.vehicle.attitude.yaw * (180/math.pi)
        status.NowLat = self.vehicle.location.global_frame.lat
        status.NowLon = self.vehicle.location.global_frame.lon
        status.Alt = int(self.vehicle.location.global_relative_frame.alt)
        status.speed = int(math.sqrt(math.pow(self.vehicle.velocity[0], 2) + math.pow(self.vehicle.velocity[1], 2)))
        status.Bettery = int(self.vehicle.battery.voltage * 10)

        send = int(status.NowLat * 10000000)
        Data[0] = self.__uint7(send, 28)
        Data[1] = self.__uint7(send ,21)
        Data[2] = self.__uint7(send, 14)
        Data[3] = self.__uint7(send, 7)
        Data[4] = self.__uint7(send, 0)

        send = int(status.NowLon * 10000000)
        Data[5] = self.__uint7(send, 28)
        Data[6] = self.__uint7(send, 21)
        Data[7] = self.__uint7(send, 14)
        Data[8] = self.__uint7(send, 7)
        Data[9] = self.__uint7(send, 0)
        Data[10] = self.__uint7(status.Alt, 7)
        Data[11] = self.__uint7(status.Alt, 0)
        Data[14] = self.__uint7(status.speed,7)
        Data[15] = self.__uint7(status.speed,0)
        Data[12] = self.__uint7(status.Bettery,7)
        Data[13] = self.__uint7(status.Bettery,0)

        # print(status.Roll, status.Pitch, status.Yaw, status.NowLat, status.NowLon, status.Alt, status.speed,status.Bettery)
        
        return 0
    
    def SetMode(self, Cmd):
        if(Cmd.Commend == 4): # 시동
            print('시동')
            self.vehicle.armed = True

        elif(Cmd.videoObjectCenterH == 0 and Cmd.videoObjectCenterW == 0 and Cmd.Commend == 3):
            print('가이드 모드')
            self.vehicle.mode = VehicleMode("GUIDED")  # 가이드 모드

        elif(Cmd.Commend == 2):
            print('복귀')
            self.vehicle.mode = VehicleMode("RTL") # 복귀

        elif(Cmd.Commend == 1): # 이륙
            print('이륙')
            self.vehicle.simple_takeoff(4)

    def Sendcommand(self, Cmd, status, Angle, O_newgps):
        # print(Cmd.Commend)
        # elif(Cmd.videoObjectCenterH == 0 and Cmd.videoObjectCenterW == 0 and Cmd.Commend == 5): # 이동
        #     self.mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, self.target_system, self.target_component,
        #                                                                      mavutil.mavlink.MAV_FRAME_GLOBAL_TERRAIN_ALT_INT , int(0b110111111000),  Cmd.CommendLat, Cmd.CommendLon, 15, 0,0,0, 0,0,0, 0,0))
        
        if(Cmd.videoObjectCenterH != 0 and Cmd.videoObjectCenterW != 0 and Cmd.Commend == 5):
            if(O_newgps[0] != 0 and O_newgps[1] != 0):
                if(Angle[2] < 0):
                    Angle[6] -= 180
                
                msg = self.vehicle.message_factory.command_long_encode(
                    0, 0,    # target system, target component
                    mavutil.mavlink.MAV_CMD_CONDITION_YAW,
                    0, #confirmation
                    Angle[6],    # param 1, yaw in degrees
                    0,          # param 2, yaw speed deg/s
                    0, # param 3, direction -1 ccw, 1 cw
                    0, # param 4, relative offset 1, absolute angle 0
                    0, 0, 0)    # param 5 ~ 7 not used
                self.vehicle.send_mavlink(msg)

                msg = self.vehicle.message_factory.set_position_target_global_int_encode(
                    0,       # time_boot_ms (not used)
                    0, 0,    # target system, target component
                    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
                    int(0b100111111000), # type_mask (only speeds enabled)
                    O_newgps[0], O_newgps[1], 4,
                    0, # X velocity in NED frame in m/s
                    0, # Y velocity in NED frame in m/s
                    0, # Z velocity in NED frame in m/s
                    0, 0, 0, # afx, afy, afz acceleration
                    (math.pi * (Angle[6] / 180)), 0
                )
                self.vehicle.send_mavlink(msg)
        return
    
class Status:
    def __init__(self):
        self.Roll = 0
        self.Pitch = 0
        self.Yaw = 0
        self.Bettery = 0
        self.NowLon = 0
        self.NowLat = 0
        self.Alt = 0
        self.speed = 0

class Commend:
    def __init__(self):
        self.videoObjectCenterH = 0
        self.videoObjectCenterW = 0
        self.Commend = 0
        self.CommendLat = 0
        self.CommendLon = 0
        self.heigth = 10
