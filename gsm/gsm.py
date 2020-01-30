# gsm module
import serial
import time

class gsm:
    def debug(self,reply):
        if self.verbose :
            print('debug:---',reply)

    def __init__(self,verbose=True):
        self.verbose = verbose
        
        self.host = 'evilcar.herokuapp.com' # the URL of the server 
        self.request = '/speed?lat=31.205753&long=29.924526'
        self.apn = "internet.etisalat"
        self.port = 80


        self.serial_port='/dev/ttyUSB0'
        self.ser=serial.Serial(self.serial_port, baudrate=115200, timeout=5)
        #check the GSM+GPRS module 
        self.ser.write(str.encode('AT'+'\r\n'))
        time.sleep(2)    
        reply=self.ser.readline()
        print(reply)  
        self.debug(reply)
        time.sleep(1)    
        
        # disconnect any existing wirless connection
        self.ser.write(str.encode('AT+CIPSHUT'+'\r\n'))
        time.sleep(2)
        reply=self.ser.read(self.ser.inWaiting())
        self.debug(reply)     
        time.sleep(1)

    def isready(self,ser):
    ''' set all current parameters to user defined profile'''
        ser.write(str.encode('ATZ'+'\r\n'))
        time.sleep(2)
        reply=ser.read(ser.inWaiting())
        self.debug(reply)     
        time.sleep(1)
    
    def connectgsm(self,ser,apn):
    ''' start task and set apn user id , password'''
        ser.write("AT+CSTT="+ apn +'"",""'+str.encode('\r\n'))
        time.sleep(2)
        reply=ser.read(ser.inWaiting())
        self.debug(reply)     
        time.sleep(1)
        #bringing up network
        ser.write('AT+CIICR'+str.encode('\r\n'))
        time.sleep(2)
        reply=ser.read(ser.inWaiting())
        while reply!='OK' :
                reply=ser.read(ser.inWaiting())
        self.debug(reply)     
        time.sleep(1)

        # getting IP address
        ser.write('AT+CIFSR'+str.encode('\r\n'))
        time.sleep(3)
        reply=ser.read(ser.inWaiting())
        self.debug(reply)     
        time.sleep(1)
        # returning all messages from modem
        reply=ser.read(ser.inWaiting())
        self.debug(reply)     
        return reply

    def connectTCP(self,ser, host , port):
    ''' connect to the tcp'''
        ser.write('AT+CIPSTART="TCP"',+ host +","+str.encode(port)+str.encode('\r\n'))
        time.sleep(5)
        reply=ser.read(ser.inWaiting())
        while reply!='OK':
                reply=ser.read(ser.inWaiting())
        self.debug(reply)
        return reply     
        time.sleep(1)

    def sendHTTPRequest(self,ser,host,request):
    ''' send function'''
        ser.write('AT+CIPSEND'+'\r\n')
        time.sleep(2)
        request ="GET " + request +str.encode("HTTP/1.1\r\nHost:"+ host + "\r\n\r\n")
        ser.write(request + chr(26))
        time.sleep(2)
    
    def closeTCP(self,ser,showresponse=False):
    ''' close TCP'''
        ser.write('AT+CIPCLOSE=1'+'\r\n')
        reply=ser.read(ser.inwaiting())
        if showresponse:
            print ("server response:\n" + reply[(reply.index("SEND OK") + 9):])
        time.sleep(2)        

    def getIPstatus(self,ser):
    ''' get IPStatus'''
        ser.write('AT+CIPSTATUS'+str.encode('\r\n'))
        time.sleep(1)
        reply=ser.read(ser.inWaiting())
        return reply                




