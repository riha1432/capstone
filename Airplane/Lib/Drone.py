import ray
import asyncio
import math
from dronekit import connect, VehicleMode, Command, LocationGlobal
from pymavlink import mavutil
from pymavlink.dialects.v20 import common

import Lib.Status as STATUS

@ray.remote
class DRONE:
    def __init__(self):
        self.ID : int = 0
        self.Target_System: int = 0
        self.Target_Component: int = 0
        self.vehicle = None
        self.status: STATUS.Status = STATUS.Status()

    def connect(self, address, id = 0) -> bool:
        self.ID = id

        print("========Drone connecting========")
        while True:
            try:
                self.vehicle = connect(address, wait_ready=True)
                print("       Drone connection complete       ")
                return 1
            except:
                pass
        return 0
    
    def receive(self) -> STATUS.Status:
        self.status.Roll = self.vehicle.attitude.roll * (180/math.pi)
        self.status.Pitch = self.vehicle.attitude.pitch * (180/math.pi)
        self.status.Yaw = self.vehicle.attitude.yaw * (180/math.pi)
        self.status.NowLat = self.vehicle.location.global_frame.lat
        self.status.NowLon = self.vehicle.location.global_frame.lon
        self.status.Alt = int(self.vehicle.location.global_relative_frame.alt)
        self.status.speed = int(math.sqrt(math.pow(self.vehicle.velocity[0], 2) + math.pow(self.vehicle.velocity[1], 2)))
        self.status.Bettery = int(self.vehicle.battery.voltage * 10)

        return self.status
    
    
