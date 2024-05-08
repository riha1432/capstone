import math

def get_location_metres(original_location, Distance):

    earth_radius = 6378137.0 

    # Coordinate offsets in radians
    dLat = Distance[4] / earth_radius
    dLon = Distance[5] / (earth_radius * math.cos(math.pi * original_location.NowLat/180))

    # New position in decimal degrees
    newlat = original_location.NowLat + (dLat * 180/math.pi)
    newlon = original_location.NowLon + (dLon * 180/math.pi)

    return [int(newlat * 10000000), int(newlon * 10000000)]


def get_distance_metres(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon

    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5


def get_bearing(aLocation1, aLocation2):
    off_x = aLocation2.lon - aLocation1.lon
    off_y = aLocation2.lat - aLocation1.lat
    bearing = 90.00 + math.atan2(-off_y, off_x) * 57.2957795

    if bearing < 0:
        bearing += 360.00

    return bearing