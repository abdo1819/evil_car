import numpy as np
import time
import scipy
from scipy import integrate
import time
import board
import busio
import adafruit_adxl34x
from Queue import Queue
# ##############integration tutriall
# x = np.linspace(0, np.pi*2.0,4097)
# y = np.square(np.square(np.sin(x)))
# print(x)

# integrate.romb(y,dx=np.pi*2.0/4097)

#best value for samples romb integration is >  4096
#note about romb : samples number must be in form 2**k+1

class accel:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.accelerometer = adafruit_adxl34x.ADXL345(i2c)
        self.counter = 0


    def calc_speed(self,arrx,step,arry=None,arrz=None):
        if(type(arry)!=None and type(arrz)!=None ):
            return (integrate.romb(arrx,dx=step),   integrate.romb(arry,dx=step) ,   integrate.romb(arrz,dx=step))
        return integrate.romb(arrx,dx=step)

    def add_acc_val(self,arrx,combred_time,period,arry=None,arrz=None,long_arr=None,lat_arr=None):
        """
        get values from  sensor
        
        """
        
        while time.time()-combred_time<period :
            pass 
        arrx[0,self.counter]=self.accelerometer.acceleration[0]
        if(type(arry)!=type(None)):
            arry[0,self.counter]=self.accelerometer.acceleration[1]
        if(type(arrz)!=type(None)):
            arrz[0,self.counter]=self.accelerometer.acceleration[2]
        if(type(lat_arr)!=type(None)):
            lat_arr[counter]=0#read gps _____________________review kerolos girgs code__________________
        if(type(long_arr)!=type(None)):
            long_arr[counter]=0#read gps _____________________review kerolos girgs code__________________
            
        self.counter=self.counter+1
        if self.counter>4096:
            self.counter=0
    
    def smooth_accl(self,arrx,arry=None,arrz=None):
        maxX=np.max(arrx)+1
        print(maxX)
        arrx=arrx*np.abs(arrx)/maxX
        print(str(type(arry)))
        if type(arry) !=type(None) :
            maxY=np.max(arry)+1
            arry=arry*np.abs(arry)/maxY
                
        if type(arrz) !=type(None) :
            maxZ=np.max(arrz)+1
            arrz=arrz*np.abs(arrz)/maxZ
    def detect_humbs(self,arrz,arrx,long_arr,lat_arr):
        """
        humps make change in z axis in short period
        make sure that max vlaue of hump is about 0.8g (car is falling )
        make sur that hump occured in only small amount of time
        """
        if np.abs(np.abs(np.max(arrz))-9.8) > 0.8*9.8 :
            low = np.where(arrz < 0.15*9.8)
            if len(low)/len(arrz) >= 0.7:
                print ("humb")
                return True , (lat_arr(np.argmax(arrz)),long_arr(np.argmax(arrz)))
        print("noHumps")
        return False , (lat_arr(np.argmax(arrz)),long_arr(np.argmax(arrz))),np.argmax(arrz)
    
    def test(self):        
        ######################### 1st test  ##################################    
        arr=np.ones((1,20))

        arr[0,5]=1
        print(arr)
        arr2=np.ones(((1,20)))*5
        arr2[0,5]=985


        self.smooth_accl(arr,arr2)
        print(arr)       
        print(arr2)        
        self.detect_humbs(arr,arr2)
        ##################################################################
    ###############  what  happens in project  ########################
    def get_humb_speed(self):
        # speedAcc=0
        #########read gps _____________________review kerolos girgs code__________________
        ##first time
        #######sleep 4 seconds by reading accelration
        # start=time.time()
        while True:
            arrx=np.zeros((1,4097))
            arry=np.zeros((1,4097))
            arrz=np.zeros((1,4097))
            arr_long=np.zeros((1,4097))
            arr_lat=np.zeros((1,4097))
            print("2nd test")
            for i in range (4097):
                self.add_acc_val(arrx,time.time(),0.001/12,arry,arrz,arr_long,arr_lat)
                # end=time.time()#########extra seconds why?????????????????         
            self.smooth_accl(arrx,arry,arrz)
            return self.detect_humbs(arrz,arrx)#hump detect
        
        # print(speed_accelometer)
    #########read gps _____________________review kerolos girgs code__________________
      ##  second time
    ######apply kalman filter
queue_accl=Queue(10)
class accelThreadProduce :
    def __init__(self):
        self.humb=false
        self.speed=(0,0)
        self.reader=accel()
        super(accelThread, self).__init__()
        
    def run(self):
        
        while True:
            global queue_accl 
            queue_accl.put(reader.get_humb_speed())
            
            
        
class accelThreadConsume(Thread):
    def run(self):
        global queue
        while True:
            values = queue_accl.get()
            queue_accl.task_done()
            if values[1]==True:
                ##gsm invoke _____review salma emad code________
                
                

