import ray
import asyncio

@ray.remote
class PARALLEL_PROCESSING:
    def __init__(self, server_address, server_port, drone_port, camera_port):
        self.Server = None
        self.Drone = None
        self.Camera = None