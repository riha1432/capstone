from pymavlink import mavutil
from Error import Error

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
        self.Mav_Message.append(mavutil.mavlink.MAVLINK_MSG_ID_RC_CHANNELS) #// 65
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
            self.mavlin.target_system,
            self.mavlin.target_component,
            mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
            0,  # confirmation
            self.Mav_Message[rq],
            0, 0, 0, 0, 0, 0  # unused parameters
        )
        return

    def Receive(self, Data):
        self.msg = self.mavlin.recv_match()
        
        if(self.msg != None):
            if(self.msg.get_type() == "LOCAL_POSITION_NED"):
                # print(self.msg)
                Data[10] = self.__uint7(int(-self.msg.z), 7)
                Data[11] = self.__uint7(int(-self.msg.z), 0)
                return 0
            
            if(self.msg.get_type() == "GLOBAL_POSITION_INT"):
                # print(self.msg)
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
            
            elif(self.msg.get_type() == "RC_CHANNELS"):
                # print(self.msg)
                return 2
            
            elif(self.msg.get_type() == "VFR_HUD"):
                # print(self.msg)
                speed = int(self.msg.groundspeed * 10)
                Data[14] = self.__uint7(speed,7)
                Data[15] = self.__uint7(speed,0)
                return 3
            
            elif(self.msg.get_type() == "BATTERY_STATUS"):
                # print(self.msg)
                vol = int(self.msg.voltages[0]/100)
                Data[12] = self.__uint7(vol,7)
                Data[13] = self.__uint7(vol,0)
                return 4
 
        return -1
    
    def Sendcommand(self, data = 0):
        return