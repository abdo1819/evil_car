# from gps.gps import gps
from  gps.gps__ import gps 
import time as t
from accel import accel
 
from serial import Serial 
g = gps()

accel_module = accel()

# speed_module= accel()
speed_limit = 1
long1=0
lat1=0
long2=0
lat2=0
print("****")
while True:
    print("hey")    
    if(long1 != -1 or lat1!= -1 ):
        lat1,long1=g.GPS_Info()
    
    t1=t.time()
    humb,speedacc = accel_module.get_humb_speed()
    print("_______accl",speedacc,humb)
    t.sleep(2)
    if(long1 != -1 or lat1!= -1 ):
    
        lat2,long2= g.GPS_Info()
    time = t1 - t.time()
    
    speed = g.get_speed(lat1,long1,lat2,long2,time)
    
    print("speed___GPS",speed)
    speed_limit = 5
    if(speed >speed_limit):    
        print(lat1,lat2,long1,long2)
# speed = g.getspeed()

