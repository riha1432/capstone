import math

class a:
    def __init__(self):
        self.lat = -35.000000
        self.lon = 149.0000000


original_location = a()

earth_radius = 6378137.0 

# Coordinate offsets in radians
dLat = 3 / earth_radius
dLon = 3 / (earth_radius * math.cos(math.pi * original_location.lat/180))

# New position in decimal degrees
newlat = original_location.lat + (dLat * 180/math.pi)
newlon = original_location.lon + (dLon * 180/math.pi)

print(newlat, newlon)

dlat = newlat - original_location.lat
dlong = newlon - original_location.lon

print(math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5)

bearing = 90.00 + math.atan2(-dlat, dlong) * 57.2957795

if bearing < 0:
    bearing += 360.00

print(bearing)