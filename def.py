import numpy as np
import time
from scipy import integrate
import time
import board
import busio
import adafruit_adxl34x
# ##############integration tutriall
# x = np.linspace(0, np.pi*2.0,4097)
# y = np.square(np.square(np.sin(x)))
# print(x)

# integrate.romb(y,dx=np.pi*2.0/4097)

#best value for samples romb integration is >  4096
#note about romb : samples number must be in form 2**k+1
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
def calc_speed(arrx,step,arry=None,arrz=None):
    if(type(arry)!=None and type(arrz)!=None ):
          return (integrate.romb(arrx,dx=step),   integrate.romb(arry,dx=step) ,   integrate.romb(arrz,dx=step))
    return integrate.romb(arrx,dx=step)
def add_acc_val(arrx,combred_time,period,arry=None,arrz=None):
    """
    get values from  sensor
    
    """
    global counter
    
    while time.time()-combred_time<period :
        pass 
    arrx[0,counter]=accelerometer.acceleration[0]
    if(type(arry)!=type(None)):
        arry[0,counter]=accelerometer.acceleration[1]
    if(type(arrz)!=type(None)):
        arrz[0,counter]=accelerometer.acceleration[2]
    counter=counter+1
    if counter>4096:
        counter=0
def smooth_accl(arrx,arry=None,arrz=None):
    maxX=np.max(arrx)
    print(maxX)
    arrx=arrx*np.abs(arrx)/maxX
    print(str(type(arry)))
    if type(arry) !=type(None) :
        maxY=np.max(arry)
        arry=arry*np.abs(arry)/maxY
             
    if type(arrz) !=type(None) :
        maxZ=np.max(arrz)
        arrz=arrz*np.abs(arrz)/maxZ
def detect_humbs(arrz,arrx):
    """
    humps make change in z axis in short period
    make sure that max vlaue of hump is about 0.8g (car is falling )
    make sur that hump occured in only small amount of time
    """
    if np.abs(np.max(arrz)) > 0.8*9.8 :
        low = np.where(arrz < 0.15*9.8)
        if len(low)/len(arrz) >= 0.7:
            print ("humb")
            return True
    print("noHumps")
    return False    
            
    
    
    
    
    
######################### 1st test  ##################################    
arr=np.ones((1,20))

arr[0,5]=1
print(arr)
arr2=np.ones(((1,20)))*5
arr2[0,5]=985


smooth_accl(arr,arr2)
print(arr)       
print(arr2)        
detect_humbs(arr,arr2)
##################################################################


###############  what  happens in project  ########################

speedAcc=0
#########read gps first time
#######sleep 4 seconds by reading accelration
start=time.time()
while True:

    arrx=np.zeros((1,4097))
    arry=np.zeros((1,4097))
    arrz=np.zeros((1,4097))
    print("2nd test")
    for counter in range (4097):
        add_acc_val(arrx,time.time(),0.001,arry,arrz)
        end=time.time()#########extra seconds why?????????????????



    


    smooth_accl(arrx,arry,arrz)
    detect_humbs(arrz,arrx)#hump detect
    speed_accelometer=calc_speed(arrx,.001,arry,arrz)
    print(speed_accelometer)
#########read gps second time
######apply kalman filter 
