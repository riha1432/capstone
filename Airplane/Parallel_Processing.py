import ray
import asyncio

import Lib.Server as SERVER
import Lib.Drone as DRONE
import Lib.Commend as COMMEND

@ray.remote
class PARALLEL_PROCESSING:
    def __init__(self, server_address, server_port, drone_port, camera_port):
        self.Server = SERVER.Server()
        self.Server.connect('', 8484)
        self.Drone = DRONE.Drone()
        self.Drone.connect('/dev/ttyS0', 57600)
        self.Camera = None
