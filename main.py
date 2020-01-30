# from gps.gps import gps
from accel.deffrential import accel

# gps_module = gps()
accel_module = accel()

while True:
    humb,speed = accel_module.get_humb_speed()
    print(speed,humb)
    # speed = g.getspeed()