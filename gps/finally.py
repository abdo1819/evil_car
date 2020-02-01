
m serial import Serial              #import serial pacakge
from time 
from time import sleep  
from math import radians, cos, sin, asin, sqrt,atan2,degrees
import webbrowser           #import package for opening link in browser
import sys                  #import system package

class gps:
    def __init__(self):
        self.gpgga_info = "$GPGGA,"
        self.ser = Serial("/dev/ttyUSB0", baudrate = 115200 )
        self.GPGGA_buffer = 0
        self.NMEA_buff = 0
        self.lat_in_degrees = 0
        self.long_in_degrees = 0
        self.nmea_latitude = 0                       #extract latitude from GPGGA string
        self.nmea_longitude = 0
        self.nmea_n_s=014
        self.nmea_e_w=0
        self.pointA =0
        self.pointB =0
        self.lat_1=0
        self.long_1=0
        self.lat_2=0
        self.long_2=0
        # self.ser.write( str.encode('AT+GPS=1'+'\r\n'))            # open gps
        # # ser.write(str.encode('AT+AGPS=1'+'\r\n'))            # open gps
        # sleep(5)
        # self.ser.write(str.encode('AT+GPSRD=3'+'\r\n'))
        # # receive= ser.read(100)
        
    def GPS_Info(self):
        '''
        calculate latitude and  longitude 
         return lat_in_degrees , long_in_degrees

        '''
        
        ser.write(str.encode('AT+AGPS=1'+'\r\n'))            # open gps
        sleep(5)
        ser.write(str.encode('AT+GPSRD=3'+'\r\n'))

        received_data = (str)(ser.readline())
        print(received_data)                 #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string
        
        while (GPGGA_data_available>0 and time_out<2000):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string
            NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
            time_out+=1

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
        if nmea_latitude=="" :
            nmea_latitude=0
        if nmea_longitude=="" :
            nmea_longitude=0
        # print((nmea_latitude,nmea_longitude,"***"))
        lat = float(nmea_latitude)              #convert string into float for calculation
        longi = float(nmea_longitude)           #convertr string into float for calculation

        lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
        long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
        
        return lat_in_degrees , long_in_degrees

    #convert raw NMEA string into degree decimal format
    def convert_to_degrees(self,raw_value):
        gpgga_info = self.gpgga_info
        ser = self.ser
        GPGGA_buffer = self.GPGGA_buffer
        NMEA_buff = self.NMEA_buff
        lat_in_degrees = self.lat_in_degrees
        long_in_degrees = self.long_in_degrees
        nmea_latitude = self.nmea_latitude
        nmea_longitude = self.nmea_longitude
        nmea_n_s = self.nmea_n_s
        nmea_e_w = self.nmea_e_w
        pointA = self.pointA
        pointB = self.pointB
        lat_1 = self.lat_1
        long_1 = self.long_1
        lat_2 = self.lat_2
        long_2 = self.long_2

        decimal_value = raw_value/100.00
        degrees = int(decimal_value)
        # mm_mmmm = ( int(decimal_value) - decimal_value )/0.6  #accuricy not sure
        mm_mmmm = ( decimal_value - int(decimal_value) )
        position = degrees + mm_mmmm
        position = "%.4f" %(position)
        return position

    #----------------------------------------test ------------------------------------------------
    # 2918'41.3"N 3050'32.2"E
    # 29.311484, 30.842286
    # -----
    # 2920'08.4"N 3053'14.8"E
    # 29.335655, 30.887433
    #----------------------------------------test ------------------------------------------------
    def get_speed(self,lat_in_degrees_1 , long_in_degrees_1 , lat_in_degrees_2 , long_in_degrees_2):
        gpgga_info = self.gpgga_info
        ser = self.ser
        GPGGA_buffer = self.GPGGA_buffer
        NMEA_buff = self.NMEA_buff
        lat_in_degrees = self.lat_in_degrees
        long_in_degrees = self.long_in_degrees
        nmea_latitude = self.nmea_latitude
        nmea_longitude = self.nmea_longitude
        nmea_n_s = self.nmea_n_s
        nmea_e_w = self.nmea_e_w
        pointA = self.pointA
        pointB = self.pointB
        lat_1 = self.lat_1
        long_1 = self.long_1
        lat_2 = self.lat_2
        long_2 = self.long_2
        start= time.time()
        # self.GPS_Info()
        # lat_1=lat_in_degrees
        # long_1=long_in_degrees
        
        # sleep(3)

        # self.GPS_Info()
        # lat_2=lat_in_degrees
        # long_2=long_in_degrees

        end = time.time()
        dLat = radians(lat_in_degrees_2  - lat_in_degrees_1)
        dLon = radians(long_in_degrees_2 - long_in_degrees_1)
        lat_1_radians = radians(lat_in_degrees_1)
        lat_2_radians = radians(lat_in_degrees_2)

        a = sin(dLat/2)**2 + cos(lat_1_radians)*cos(lat_2_radians)*sin(dLon/2)**2
        c = 2*asin(sqrt(a))
        R = 6372.8
        km = R*c
        time =start-end                      #  get time in second 
        time = "%.4f" %(time)
        speed = km/(time/ (60*60))
        speed = "%.4f" %(speed)
        return speed

        # ------------------------------------------------------------
    def initial_bearing(self,lat_in_degrees_1 , long_in_degrees_1 , lat_in_degrees_2 , long_in_degrees_2):
        gpgga_info = self.gpgga_info
        ser = self.ser
        GPGGA_buffer = self.GPGGA_buffer
        NMEA_buff = self.NMEA_buff
        lat_in_degrees = self.lat_in_degrees
        long_in_degrees = self.long_in_degrees
        nmea_latitude = self.nmea_latitude
        nmea_longitude = self.nmea_longitude
        nmea_n_s = self.nmea_n_s
        nmea_e_w = self.nmea_e_w
        pointA = self.pointA
        pointB = self.pointB
        lat_1 = self.lat_1
        long_1 = self.long_1
        lat_2 = self.lat_2
        long_2 = self.long_2

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

        return compass_bearing
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
    #     pointA = (lat_1, long_1)
    #     pointB = (lat_2, long_2)
    #         while True:

    #                 initial_bearing(pointA, pointB)

    #                 speed = get_speed()
    #                 return speed
    #                 print("your speed : ",speed ,"km/h" )                                   #

    #                 print("lat in degrees:", str(lat_in_degrees)," long in degree: ", str(long_in_degrees), '\n')
    #                 map_link = 'http://maps.google.com/?q=' + str(lat_in_degrees) + ',' + str(long_in_degrees)    #create link to plot location on Google map
    #                 print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")               #press ctrl+c to plot on map and exit
    #                 print("------------------------------------------------------------\n")
    #     #        else :
    #     #           ser.write( str.encode('AT+GPS=1'+'\r\n'))            # open gps
    #     #          # ser.write(str.encode('AT+AGPS=1'+'\r\n'))            # open gps
    #     #         sleep(5)
    #         #        ser.write(str.encode('AT+GPSRD=3'+'\r\n'))

    #     except KeyboardInterrupt:
    #         webbrowser.open(map_link)                                   #open current position information in google map
    #         sys.exit(0)
