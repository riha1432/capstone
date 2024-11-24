import math

LEFT_RIGHT_ANGLE_OF_VIEW = 100
UP_DOWN_ANGLE_OF_VIEW = 90
CAMERA_ANGLE = 45
EARTH_RADIUS = 6378137.0 

class Distance_estimate:
    def __init__(self, picture_quality : list):
        self.pixel_angleH: float= (UP_DOWN_ANGLE_OF_VIEW / picture_quality[0])
        self.pixel_angleW: float = (LEFT_RIGHT_ANGLE_OF_VIEW / picture_quality[1])
        self.angle45_distance: list = [0 for _ in range(3)]
        self.angle45_gps: list = [0 for _ in range(3)]
        self.object_distance: list = [0 for _ in range(3)]
        self.object_gps: list = [0 for _ in range(3)]

    def __get_Distance_to_gps(self, Now_Gps, Distance):
        dLat = Distance[0] / EARTH_RADIUS
        dLon = Distance[1] / (EARTH_RADIUS * math.cos(math.pi * Now_Gps[0]/180))

        newlat = Now_Gps[0].NowLat + (dLat * 180/math.pi)
        newlon = Now_Gps[0].NowLon + (dLon * 180/math.pi)

        return [int(newlat * 10000000), int(newlon * 10000000)]
    
    
