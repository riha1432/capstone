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

# mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, target_system, target_component,
#                                                                                 mavutil.mavlink.MAV_FRAME_GLOBAL_TERRAIN_ALT_INT, int(0b100111111000), -353626798, 1491658202, 15, 0,0,0, 0,0,0, (math.pi * (45 / 180)), 0))

msg = vehicle.message_factory.set_position_target_global_int_encode(
                    0,       # time_boot_ms (not used)
                    0, 0,    # target system, target component
                    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
                    int(0b100111111000), # type_mask (only speeds enabled)
                    -353626798, 1491658202, 15,
                    0, # X velocity in NED frame in m/s
                    0, # Y velocity in NED frame in m/s
                    0, # Z velocity in NED frame in m/s
                    0, 0, 0, # afx, afy, afz acceleration
                    0, 0
                )
vehicle.send_mavlink(msg)
# status.Roll = self.msg.roll * (180/math.pi)
#                 status.Pitch = self.msg.pitch * (180/math.pi)
#                 status.Yaw = self.msg.yaw * (180/math.pi)
# while True:
#     Roll = vehicle.attitude.roll * (180/math.pi)
#     Pitch = vehicle.attitude.pitch * (180/math.pi)
#     Yaw = vehicle.attitude.yaw * (180/math.pi)
#     print(Roll, Pitch, Yaw)