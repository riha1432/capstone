import math

def get_location_metres(original_location, Distance):

    earth_radius = 6378137.0 

    # Coordinate offsets in radians
    dLat = Distance[0] / earth_radius
    dLon = Distance[1] / (earth_radius * math.cos(math.pi * original_location.NowLat/180))

    # New position in decimal degrees
    newlat = original_location.NowLat + (dLat * 180/math.pi)
    newlon = original_location.NowLon + (dLon * 180/math.pi)

    return [int(newlat * 10000000), int(newlon * 10000000)]


def get_distance_metres(aLocation1, aLocation2):
    dlat = aLocation1.NowLat - aLocation2[0]
    dlong = aLocation1.NowLon - aLocation2[1]

    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5


def get_bearing(aLocation1, aLocation2):
    off_x = aLocation1.NowLon - aLocation2[1]
    off_y = aLocation1.NowLat - aLocation2[0] 
    bearing = 90.00 + math.atan2(-off_y, off_x) * 57.2957795

    if bearing < 0:
        bearing += 360.00

    return bearing