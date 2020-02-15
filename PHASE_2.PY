'''
pahse 2 edited 

'''
import time
from time import sleep
from math import radians, cos, sin, asin, sqrt,atan2,degrees
import webbrowser                                           	#import package for opening link in browser
import sys                                                      #import system package
import serial

class gps:
	def __init__(self):
    	self.gpgga_info = "$GPGGA,"
    	self.ser = serial.Serial("/dev/ttyUSB0", baudrate = 115200 , timeout=6)

    	# self.ser.write(str.encode('AT+GPS=1'+'\r\n'))        	# open gps
    	# sleep(5)
    	# self.ser.write(str.encode('AT+GPSRD=1'+'\r\n'))
    	# sleep(1)
    	# received_data = (str)(self.ser.readline())
    	# print("REC",received_data) 	
    	# sleep(1)
	def GPS_Info(self):
    	print("STARTgpsINFO")
    	'''
    	calculate latitude and  longitude
     	return lat_in_degrees , long_in_degrees
    	'''
        #read NMEA string received
    	received_data = (str)(self.ser.readline())
    	time_out = 1
    	GPGGA_data_available = received_data.find(self.gpgga_info)   #check for NMEA GPGGA string
    	
    	while ( time_out<10 and GPGGA_data_available<=0):
        	received_data = (str)(self.ser.readline())
			sleep(1)
        	GPGGA_data_available = received_data.find(self.gpgga_info)   #check for NMEA GPGGA string
        	time_out+=1
            	# if (GPGGA_data_available == 0 ):
    	time_out = 1
    	if(GPGGA_data_available>0):

            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string
            NMEA_buff = (GPGGA_buffer.split(',')) 	
            print("nema:",NMEA_buff)                        	#store comma separated data in buffer
            #print("time out no data ")
            nmea_time = []
            nmea_latitude = []
            nmea_longitude = []
            nmea_time = NMEA_buff[0]                         	#extract time from GPGGA string
            nmea_latitude = NMEA_buff[1]                     	#extract latitude from GPGGA string
            nmea_longitude = NMEA_buff[3]                    	#extract longitude from GPGGA string
        
            print("NMEA Time: ", nmea_time,'\n')
            print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
            if nmea_latitude=="" :
                    nmea_latitude=0
            if nmea_longitude=="" :
                    nmea_longitude=0
            # print((nmea_latitude,nmea_longitude,"***"))
            lat = float(nmea_latitude)                     	    #convert string into float for calculation
            long = float(nmea_longitude)                   	    #convertr string into float for calculation

            lat_in_degrees = self.convert_to_degrees(lat)	    #get latitude in degree decimal format
            long_in_degrees = self.convert_to_degrees(long)     #get longitude in degree decimal format

            return lat_in_degrees , long_in_degrees

            print("ENDgpsINFO")
    	return -1 ,-1                                      
	def convert_to_degrees(self,raw_value,accu):                    #convert raw NMEA string into degree decimal format
		if accu > 1.0 :
            raise AttributeError
    	decimal_value = raw_value/100.00
    	degrees = int(decimal_value)
    	mm_mmmm = ( decimal_value - int(decimal_value) )/accu    #accuricy you need 
    	# mm_mmmm = ( decimal_value - int(decimal_value) )
    	position = degrees + mm_mmmm
    	position = "%.4f" %(position)
    	return float(position)

	def get_speed(self,lat_in_degrees_1 , long_in_degrees_1 , lat_in_degrees_2 , long_in_degrees_2,time):
    	dLat = radians(lat_in_degrees_2  - lat_in_degrees_1)
    	dLon = radians(long_in_degrees_2 - long_in_degrees_1)
    	lat_1_radians = radians(lat_in_degrees_1)
    	lat_2_radians = radians(lat_in_degrees_2)

    	a = sin(dLat/2)**2 + cos(lat_1_radians)*cos(lat_2_radians)*sin(dLon/2)**2
    	c = 2*asin(sqrt(a))
    	R = 6372.8
    	km = R*c
    	time = float("%.4f" %(time))
    	speed = km/(time/ (60*60))
    	speed = float("%.4f" %(speed))
    	if(long_in_degrees_1==-1 or long_in_degrees_2==-1 or lat_in_degrees_2==-1 or lat_in_degrees_1==-1):
        	return -1
    	return speed
	def initial_bearing(self,lat_in_degrees_1 , long_in_degrees_1 , lat_in_degrees_2 , long_in_degrees_2):

    	pointA = (lat_in_degrees_1, long_in_degrees_1)
    	pointB = (lat_in_degrees_2, long_in_degrees_2)

    	if (type(pointA) != tuple) or (type(pointB) != tuple):
        	raise TypeError("Only tuples are supported as arguments")

    	lat1 = radians(pointA[0])
    	lat2 = radians(pointB[0])

    	diffLong = radians(pointB[1] - pointA[1])

    	x = sin(diffLong) * cos(lat2)
    	y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(diffLong))

    	initial_bearing = atan2(x, y)

    	# Now we have the initial bearing but math.atan2 return values
    	# from -180 to + 180 which is not what we want for a compass bearing
    	# The solution is to normalize the initial bearing as shown below
    	initial_bearing = degrees(initial_bearing)
    	compass_bearing = (initial_bearing + 360) % 360
    	
    	toli = 3
    	pi=180
    	angle = compass_bearing
    	if (angle < -toli and angle < toli):
        	direction="N"

    	elif (angle > pi/2 -toli and angle < pi/2 + toli):
        	direction= "E"
    	elif (angle > pi - toli and angle < pi + toli):
        	direction= "S"
    	elif (angle > ((3*pi)/2) - toli and angle < ((3*pi)/2) + toli):
        	direction="W"

    	if (angle > 0 and angle < pi/2):
        	direction= "NE"
    	elif (angle > pi/2 and angle < pi):
        	direction="SE"
    	elif (angle > pi and angle < ((3*pi)/2) ) :
        	direction="SW"
    	elif (angle > ((3*pi)/2) and angle < 2*pi ) :
        	direction="NW"
    	else:
        	direction="not defind"

    	print ("angle:",angle,"direction:",direction)

    	return angle , direction



	#----------------------------------------test ------------------------------------------------
	# speed = get_speed()
	# print("your speed : ",speed )

	# dr= calculate_initial_compass_bearing(pointA, pointB)
	# print("your direction : ", dr )
	# # if (receive=="ok"||receive=="OK")
	#----------------------------------------test ------------------------------------------------

	# def main(self):
	# 	pointA = (lat_1, long_1)
	# 	pointB = (lat_2, long_2)
	#     	while True:

	#             	initial_bearing(pointA, pointB)

	#             	speed = get_speed()
	#             	return speed
	#             	print("your speed : ",speed ,"km/h" )                               	#

	#             	print("lat in degrees:", str(lat_in_degrees)," long in degree: ", str(long_in_degrees), '\n')
	#             	map_link = 'http://maps.google.com/?q=' + str(lat_in_degrees) + ',' + str(long_in_degrees)	#create link to plot location on Google map
	#             	print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")           	#press ctrl+c to plot on map and exit
	#             	print("------------------------------------------------------------\n")
	# 	#    	else :
	# 	#       	ser.write( str.encode('AT+GPS=1'+'\r\n'))        	# open gps
	# 	#      	# ser.write(str.encode('AT+AGPS=1'+'\r\n'))        	# open gps
	# 	#     	sleep(5)
	#     	#    	ser.write(str.encode('AT+GPSRD=3'+'\r\n'))

	# 	except KeyboardInterrupt:
	#     	webbrowser.open(map_link)                               	#open current position information in google map

	try:
    	pass
	except TypeError:
    	pass
