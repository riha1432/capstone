import math
camAngle = 45

height = 4
pitch = 0
videoObjectCenterH = 240
videoObjectCenterW = 320

pixelAngleH = (42 / 480)
videoHC = (480 / 2) - pitch / pixelAngleH
pixelAngleH = (videoObjectCenterH - videoHC) * pixelAngleH
Cos_Distance = math.cos(math.pi * ((camAngle + pixelAngleH) / 180))
Cos_Distance = height / Cos_Distance

pixelAngleW = (75 / 640)
pixelAngleW = (videoObjectCenterW - (640 / 2)) * pixelAngleW
print(pixelAngleW)
Object_Distance = math.cos(math.pi * (pixelAngleW / 180))
Object_Distance = Cos_Distance / Object_Distance # 객채 거리

Horizontal_Distance = math.sin(math.pi * ((camAngle + pixelAngleH) / 180)) * Object_Distance # 객채 수평 겨리

RL_Distance = math.tan(math.pi * (pixelAngleW / 180))
RL_Distance = RL_Distance * Cos_Distance # 좌우 겨리

print(Object_Distance, pixelAngleW, Horizontal_Distance, RL_Distance)