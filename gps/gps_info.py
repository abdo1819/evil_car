'''
created by keroles girgis 
in 21-1-2020
------ project_detalis----------------------------------------------------------
gps module (A7（GSM/GPRS quad-band+GPS+AGPS）) 
user manual link http://www.make.net.za/wp/wp-content/datasheets/A6_A7_A6C%20User%20Manual.pdf
this code to get and disbaly speed , gps information and compass_bearing
------links_helps_in_this_code--------------------------------------------------
https://stackoverflow.com/questions/3209899/determine-compass-direction-from-one-lat-lon-to-the-other
https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
https://www.hackster.io/tinkernut/raspberry-pi-smart-car-8641ca#toc-adding-gps-5
https://www.electronicwings.com/raspberry-pi/gps-module-interfacing-with-raspberry-pi
https://gist.github.com/jeromer/2005586
------------------------------------------------------------------------------------------------------------
'''
from serial import Serial              #import serial pacakge
from time import sleep
from math import radians, cos, sin, asin, sqrt,atan2
import webbrowser           #import package for opening link in browser
import sys                  #import system package



gpgga_info = "$GPGGA,"
ser = Serial ("/dev/ttyS0")    #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0
nmea_latitude = 0                       #extract latitude from GPGGA string
nmea_longitude = 0
nmea_n_s=0
nmea_e_w=0
pointA =0
pointB =0
lat_1=0
long_1=0
lat_2=0
long_2=0
# ser.write('AT+GPS=1'+'\r\n')            # open gps 
# receive= ser.read(100)

def GPS_Info():
    # global NMEA_buff
    # global lat_in_degrees
    # global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]            #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]           #extract longitude from GPGGA string
    nmea_n_s=NMEA_buff[2]
    nmea_e_w=NMEA_buff[4]
    print("NMEA Time: ", nmea_time,'\n')
    print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
    
    lat = float(nmea_latitude)              #convert string into float for calculation
    longi = float(nmea_longitude)           #convertr string into float for calculation
    
    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = ( int(decimal_value) - decimal_value )/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position

#----------------------------------------test ------------------------------------------------
# 29°18'41.3"N 30°50'32.2"E
# 29.311484, 30.842286
# -----
# 29°20'08.4"N 30°53'14.8"E
# 29.335655, 30.887433
#----------------------------------------test ------------------------------------------------
def get_speed():
    GPS_Info()
    lat_1=lat_in_degrees
    long_1=long_in_degrees

    sleep(3) 
    GPS_Info()
    lat_2=lat_in_degrees
    long_2=long_in_degrees
  
    dlong = long_2 - long_1 
    dlat  = lat_2 - lat_1 
    a = sin(dlat/2)**2 + cos(lat_1) * cos(lat_2) * sin(dlong/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    speed = km/(3/ (60*60))
    return speed 

def calculate_initial_compass_bearing(pointA, pointB):
       
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")
    
    lat_1 = radians(pointA[0])
    lat_2 = radians(pointB[0])

    diffLong = radians(pointB[1] - pointA[1])

    x = sin(diffLong) * cos(lat_2)
    y = cos(lat_1) * sin(lat_2) - (sin(lat_1) *  cos(lat_2) *  cos(diffLong))

    initial_bearing =  atan2(x, y)

   
    # initial_bearing =  degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing



# note this is pesodo code modifi it
 
# get_Dir(lat_1, long1, lat2, long2) {
#     margin = π/90; // 2 degree tolerance for cardinal directions
#     o = lat1 - lat2;
#     a = long1 - long2;
#     angle = atan2(o,a);

#     if (angle > -margin && angle < margin):
#             return "E";
#     elseif (angle > π/2 - margin && angle < π/2 + margin):
#             return "N";
#     elseif (angle > π - margin && angle < -π + margin):
#             return "W";
#     elseif (angle > -π/2 - margin && angle < -π/2 + margin):
#             return "S";
#     }
#     if (angle > 0 && angle < π/2) {
#         return "NE";
#     } elseif (angle > π/2 && angle < π) {
#         return "NW";
#     } elseif (angle > -π/2 && angle < 0) {
#         return "SE";
#     } else {
#         return "SW";
#     }
# }

pointA = (lat_1, long_1)
pointB = (lat_2, long_2)    
#----------------------------------------test ------------------------------------------------
# speed = get_speed()
# print("your speed : ",speed )

# dr= calculate_initial_compass_bearing(pointA, pointB)
# print("your direction : ", dr )
# # if (receive=="ok"||receive=="OK")
#----------------------------------------test ------------------------------------------------

try:
    while True:
        received_data = (str)(ser.readline())                   #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
            NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
            GPS_Info()                                          #get time, latitude, longitude 

            compass_bearing= calculate_initial_compass_bearing(pointA, pointB)   # print compass bearing
            print("your direction : " , compass_bearing)
            
            
            speed = get_speed()
            print("your speed : ",speed '\n',"km/h" )                                   # 

            print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
            map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees    #create link to plot location on Google map
            print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")               #press ctrl+c to plot on map and exit 
            print("------------------------------------------------------------\n")
                        
except KeyboardInterrupt:
    webbrowser.open(map_link)                                   #open current position information in google map
    sys.exit(0)

   
