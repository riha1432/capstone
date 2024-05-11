from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil
import time, sys, argparse, math
vehicle = connect('tcp:localhost:5763', wait_ready=True)
mavlin = mavutil.mavlink_connection('tcp:localhost:5763')

target_system = mavlin.target_system
target_component = mavlin.target_component
print (" Type: %s" % vehicle._vehicle_type)
print (" Armed: %s" % vehicle.armed)
print (" System status: %s" % vehicle.system_status.state)
print (" GPS: %s" % vehicle.gps_0)
print (" GPS: %s" % vehicle.location.global_frame)
print (" Alt: %s" % vehicle.location.global_relative_frame.alt)
print (" attitude: %s" % vehicle.attitude)
print (" rangefinder: %s" % vehicle.rangefinder)
print (" bett: %s" % vehicle.battery)
print (" speed: %s" % vehicle.velocity)

mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, target_system, target_component,
                                                                                mavutil.mavlink.MAV_FRAME_GLOBAL_TERRAIN_ALT_INT, int(0b100111111000), -353623706 + 10000, 1491640311, 15, 0,0,0, 0,0,0, (math.pi * (45 / 180)), 0))
# status.Roll = self.msg.roll * (180/math.pi)
#                 status.Pitch = self.msg.pitch * (180/math.pi)
#                 status.Yaw = self.msg.yaw * (180/math.pi)
while True:
    Roll = vehicle.attitude.roll * (180/math.pi)
    Pitch = vehicle.attitude.pitch * (180/math.pi)
    Yaw = vehicle.attitude.yaw * (180/math.pi)
    print(Roll, Pitch, Yaw)