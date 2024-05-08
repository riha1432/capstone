from pymavlink import mavutil
from pymavlink.dialects.v20 import common
from Error import Error
import math


class Mavlink:
    def __init__(self):
        self.Message_Id = None
        self.Target_System = None
        self.Target_Component = None
        self.mavlin = None
        self.Mav_Message = []

    def __int32(self, x):
        if(x < 0):
            return x | 0X80000000
        else:
            return x
        
    def __uint7(self, val, bit):
        return val>>bit & 0X0000007F
    
    def Connect(self, address, baud = 0):
        self.Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED) #// 32
        self.Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT) #// 33
        self.Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE ) #// 65
        self.Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_VFR_HUD) #// 74
        self.Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_BATTERY_STATUS) #// 147

        try:
            print("drone connecting .........")
            if(baud == 0):
                self.mavlin = mavutil.mavlink_connection(address)
            else:
                self.mavlin = mavutil.mavlink_connection(address, baud=baud)
            
            self.message_id = mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE 
            self.target_system = self.mavlin.target_system
            self.target_component = self.mavlin.target_component

        except:
            Error(2)

        self.mavlin.wait_heartbeat()
        return

    def Request(self, rq):
        self.mavlin.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
            0,  # confirmation
            self.Mav_Message[rq],
            0, 0, 0, 0, 0, 0  # unused parameters
        )
        return

    def Receive(self, Data, status):
        self.msg = self.mavlin.recv_match()
        
        if(self.msg != None):
            if(self.msg.get_type() == "LOCAL_POSITION_NED"):
                # print(self.msg)
                status.Alt = -self.msg.z
                Data[10] = self.__uint7(int(-self.msg.z), 7)
                Data[11] = self.__uint7(int(-self.msg.z), 0)
                return 0
            
            if(self.msg.get_type() == "GLOBAL_POSITION_INT"):
                # print(self.msg)
                status.NowLat = self.msg.lat / 10000000.0
                status.NowLon = self.msg.lon / 10000000.0
                Data[0] = self.__uint7(self.msg.lat, 28)
                Data[1] = self.__uint7(self.msg.lat ,21)
                Data[2] = self.__uint7(self.msg.lat, 14)
                Data[3] = self.__uint7(self.msg.lat, 7)
                Data[4] = self.__uint7(self.msg.lat, 0)
                Data[5] = self.__uint7(self.msg.lon, 28)
                Data[6] = self.__uint7(self.msg.lon, 21)
                Data[7] = self.__uint7(self.msg.lon, 14)
                Data[8] = self.__uint7(self.msg.lon, 7)
                Data[9] = self.__uint7(self.msg.lon, 0)
                return 1
            
            elif(self.msg.get_type() == "ATTITUDE"):
                # print(self.msg)
                status.Roll = self.msg.roll * (180/math.pi)
                status.Pitch = self.msg.pitch * (180/math.pi)
                status.Yaw = self.msg.yaw * (180/math.pi)
                # print(status.Roll, status.Pitch, status.Yaw)
                return 2
            
            elif(self.msg.get_type() == "VFR_HUD"):
                # print(self.msg)
                status.speed = int(self.msg.groundspeed * 10)
                Data[14] = self.__uint7(status.speed,7)
                Data[15] = self.__uint7(status.speed,0)
                return 3
            
            elif(self.msg.get_type() == "BATTERY_STATUS"):
                # print(self.msg)
                status.Bettery = int(self.msg.voltages[0]/100)
                Data[12] = self.__uint7(status.Bettery,7)
                Data[13] = self.__uint7(status.Bettery,0)
                return 4
 
        return -1
    
    def Sendcommand(self, Cmd, status):

        if(Cmd.Commend == 4):
            self.mavlin.mav.command_long_send(self.target_system, self.target_component, 
                          common.MAV_CMD_COMPONENT_ARM_DISARM,0, 1,0,0,0,0,0,0)
            
        elif(Cmd.videoObjectCenterH == 0 and Cmd.videoObjectCenterW == 0 and Cmd.Commend == 3):
            self.mavlin.set_mode_apm(4, 1, 1)  # 가이드 모드

        elif(Cmd.Commend == 2):
            self.mavlin.set_mode_apm(6, 1, 1) # 복귀

        elif(Cmd.Commend == 1):
            self.mavlin.mav.command_long_send(self.target_system, self.target_component,
                                common.MAV_CMD_NAV_TAKEOFF, 0, 0,0,0,0,0,0,10)
            
        elif(Cmd.videoObjectCenterH == 0 and Cmd.videoObjectCenterW == 0 and Cmd.Commend == 5):
            self.mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, self.target_system, self.target_component,
                                                                             mavutil.mavlink.MAV_FRAME_GLOBAL_TERRAIN_ALT_INT , int(0b110111111000),  Cmd.CommendLat, Cmd.CommendLon, 15, 0,0,0, 0,0,0, 0,0))
        
        elif(Cmd.videoObjectCenterH != 0 and Cmd.videoObjectCenterW != 0 and Cmd.Commend == 5):
            self.mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, self.target_system, self.target_component,
                                                                             mavutil.mavlink.MAV_FRAME_GLOBAL_TERRAIN_ALT_INT , int(0b110111111000), status.NowLat + 0, status.NowLat + 0, 15, 0,0,0, 0,0,0, 0,0))
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
        self.videoObjectCenterH = 240
        self.videoObjectCenterW = 400
        self.Commend = 0
        self.CommendLat = 0
        self.CommendLon = 0
        self.heigth = 10

    def __uint7(self, val, bit):
        return val<<bit
    
    def setdata(self, Server_data):
        self.videoObjectCenterH = self.__uint7(Server_data[0], 7) | Server_data[1]
        self.videoObjectCenterW = self.__uint7(Server_data[2], 7) | Server_data[3]
        self.CommendLat = ( self.__uint7(Server_data[4], 28) | self.__uint7(Server_data[5], 21) | 
                        self.__uint7(Server_data[6], 14) | self.__uint7(Server_data[7], 7) | Server_data[8] )
        self.CommendLon = ( self.__uint7(Server_data[9], 28) | self.__uint7(Server_data[10], 21) | 
                        self.__uint7(Server_data[11], 14) | self.__uint7(Server_data[12], 7) | Server_data[13] )
        self.Height = self.__uint7(Server_data[14], 7) | Server_data[15]
        self.Commend = Server_data[16]