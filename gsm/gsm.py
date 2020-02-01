
#Learn more or give us feedback
# gsm module
import serial
import time

class gsm:
    def debug(self,reply):
        if self.verbose :
            print('debug:---',reply)

    def __init__(self,verbose=True):
        self.verbose = verbose
        
        self.host = '"evilcar.herokuapp.com"' # the URL of the server 
        self.request = '/speed?lat=31.205753&long=29.924526'
        self.apn = '"internet.etisalat"'
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
        ser.write(str.encode("AT+CSTT="+ apn +',"",""'+'\r\n'))
        time.sleep(2)
        reply=ser.read(ser.inWaiting())
        self.debug(reply)     
        time.sleep(1)
        #bringing up network
        ser.write(str.encode('AT+CIICR'+'\r\n'))
        time.sleep(2)
        reply=ser.read(ser.inWaiting())
       
        self.debug(reply)     
        time.sleep(1)

        # getting IP address
        ser.write(str.encode('AT+CIFSR'+'\r\n'))
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
        print("tcpConnect")
        ser.write(str.encode('at+cdnsgip='+host+'\r\n'))
        time.sleep(3)
        reply=ser.read(ser.inWaiting())
        self.debug(reply)
        time.sleep(3)
        print("___________________")
        last_char=str(reply).split(host+',"')[-1].split(".")[-1].split('"')[0]
        first_3chars=str(reply).split(host+',"')[-1].split(".")[0:3]
        ip=first_3chars[0]+'.'+first_3chars[1]+'.'+first_3chars[2]+'.'+last_char
        print(str(ip))
        time.sleep(2    )
        ser.write(str.encode('AT+CIPSTART="TCP"'+','+ str(ip) +","+str(port)+'\r\n'))
        time.sleep(2    )
        reply=ser.read(ser.inWaiting())
        self.debug(reply)

        return reply     
        time.sleep(1)

    def sendHTTPRequest(self,ser,host,request):
        ''' send function'''
        ser.write(str.encode('AT+CIPSEND'+'\r\n'))
        time.sleep(2)
        ser.write(str.encode('AT+CIPSEND'+'\r\n'))
        print(print("GET " + request +" HTTP/1.1\r\nHost:"+ host.split('"')[1] + "\r\n\r\n\r"))
        request =str.encode("GET " + request +" HTTP/1.1\r\nHost: "+ host.split('"')[1] +"\r\n"+"Connection: close"+ "\r\n\r\n\r")
        ser.write(request ) 
       
        ser.write(str.encode(chr(26)))
        time.sleep(2)
        reply=ser.read(ser.inWaiting())
        self.debug(reply)
    def closeTCP(self,ser,showresponse=False):
        ''' close TCP'''
        ser.write(str.encode('AT+CIPCLOSE=1'+'\r\n'))
        reply=ser.read(ser.inwaiting())
        if showresponse:
            print ("server response:\n" + reply[(reply.index("SEND OK") + 9):])
        time.sleep(2)        

    def getIPstatus(self,ser):
        ''' get IPStatus'''
        ser.write(str.encode('AT+CIPSTATUS'+str.encode('\r\n')))
        time.sleep(1)
        reply=ser.read(ser.inWaiting())
        return reply
