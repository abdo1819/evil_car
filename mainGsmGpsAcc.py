from gsm.gsm import gsm

gsm_ = gsm()
def send_vio(long,lat):
    gsm_.current_lat=str(lat)
    gsm_.current_long=str(long)
    gsm_.request='/report'
    gsm_.isready(gsm_.ser)
    gsm_.connectgsm(gsm_.ser,gsm_.apn)
    gsm_.connectTCP(gsm_.ser,gsm_.host,80)
    gsm_.sendHTTPRequest_POST(gsm_.ser,gsm_.host,gsm_.request)
    

# from gps.gps import gps
from  gps.gps__ import gps 
import time as t
from accel import accel
import numpy as np 
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
speedacc=(0,0)

while True:
    print("hey")    
    if(long1 != -1 or lat1!= -1 ):
        lat1,long1=g.GPS_Info()
    
    t1=t.time()
    humb,speedacctemp = accel_module.get_humb_speed()
    speedacc=speedacctemp+speedacc
    speedaccsqrt=np.sqrt(np.power(speedacc[0],2)+np.power(speedacc[1],2))
    print("_______accl",speedaccsqrt,humb)
    t.sleep(2)
    if(long1 != -1 or lat1!= -1 ):
    
        lat2,long2= g.GPS_Info()
    time = t1 - t.time()
    
    speed = g.get_speed(lat1,long1,lat2,long2,time)
    
    print("speed___GPS",speed)
    speed_limit = 2
    if speed ==0:
        speed=speedaccsqrt[0]
    print("___act speed",speed)
    if(speed >speed_limit):    
        print("___________violate",lat1,lat2,long1,long2)
        gsm_.speed=speed
        send_vio(lat2,long2)
# speed = g.getspeed()


