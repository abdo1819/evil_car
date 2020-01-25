import numpy as np
import time
from scipy import integrate
x = np.linspace(0, np.pi*2.0,4097)
y = np.square(np.square(np.sin(x)))
print(x)
integrate.romb(y,dx=np.pi*2.0/4097)
def calc_speed(arrx,step,arry=None,arrz=None):
    if(arry!=None and arrz!=None ):
          return (integrate.romb(arrx,dx=step),   integrate.romb(arry,dx=step) ,   integrate.romb(arrz,dx=step))
    return integrate.romb(arrx,dx=step)
def add_acc_val(arrx,combred_time,period,arry=None,arrz=None):
    while time.time()-combred_time<period :
        pass 
    arrx.append(1)##use sensor library instead
    if(arry!=type(None)):
        arry.append(1)##use sensor library instead
    if(arry!=type(None)):
        arrz.append(1)##use sensor library instead

def smooth_accl(arrx,arry=None,arrz=None):
    maxX=np.max(arrx)
    print(maxX)
    for x in range(len(arrx)) :
        arrx[x]=arrx[x]*np.abs(arrx[x])/maxX
    print(str(type(arry)))
    if type(arry) !=type(None) :
        for x in range(len(arry)) :
            maxY=np.max(arry)
            arry[x]=arry[x]*np.abs(arry[x])/maxY
             
    if type(arrz) !=type(None) :
        for x in range(len(arrz)) :
            maxZ=np.max(arrz)
            arry[x]=arry[x]*np.abs(arry[x])/maxY
def detect_humbs(arrz,arrx):
    if np.abs(np.max(arrz)) > 0.8*9.8 :
        low = np.where(arrz < 0.15*9.8)
        if len(low)/len(arrz) >= 0.7:
            print ("humb")
            return True
    print("noHumps")
    return False    
            
    
    
    
    
    
#########################test##################################    
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


###############what  happens in project########################
#########read gps first time
#######sleep 4 seconds by reading accelration
start=time.time()
arrx=list()
arry=list()
arrz=list()
print("2nd test")
for counter in range (4097):
    add_acc_val(arrx,time.time(),0.001,arry,arrz)
end=time.time()#########extra seconds why?????????????????

print(end-start)
for i in range (10,100):
    arrz[i]=1.5*9.8##########make humps
smooth_accl(arrx,arry,arrz)
detect_humbs(arrz,arrx)
speed_accelometer=calc_speed(arrx,.001,arry,arrz)
print(speed_accelometer)
#########read gps second time
######apply kalman filter 
