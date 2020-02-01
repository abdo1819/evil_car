#Learn more or give us feedback
# gsm module
import serial
import time
import json as JSON 
def write_request(content_str
                ,host
                ,method="GET"
                ,path="/"
                ,content_type="application/json"
                ,new_line="\r\n"
                ,http_version="HTTP/1.1"
                ):
    return method+" "+path+" "+http_version+new_line \
        +"Host: "+host+new_line \
        +"Content-Type: "+content_type+new_line \
        +"Content-Length: "+str(len(content_str))+new_line*2 \
        +content_str \
        +new_line           
class gsm:
    def debug(self,reply):
        if self.verbose :
            print('debug:---',reply)

    def __init__(self,verbose=True):
        self.verbose = verbose
        
        self.host = '"evilcar.herokuapp.com"' # the URL of the server 
        self.current_lat='0'
        self.current_long='0'
        self.speed=0
        self.time=''
        self.id=0
        self.request = '/speed?lat='+self.current_long+'&long='+self.current_long
        self.request_post='/report'
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
         

    def sendHTTPRequest_GET(self,ser,host,request):
        ''' send function'''
        ser.write(str.encode('AT+CIPSEND'+'\r\n'))
        time.sleep(2)
        request =str.encode(write_request("",host.split('"')[1],"GET",request)+ "\r\n\r\n")
        ser.write(request )
        ser.write(str.encode(chr(26)))
        time.sleep(2)
        reply=ser.read(ser.inWaiting())
        json=[]
        res={}
        if(len(str(reply).split("{"))>0):
            if(len(str(reply).split("{")[-1])>0):
                if(len(str(reply).split("{")[-1].split('}'))>0):
                    print("yes")
                    json = str(reply).split("{")[-1].split('}')[0].split(':')
                    res = {json[i]: json[i + 1] for i in range(0, len(json), 2)} 
        #print(str(reply).split("\r\n\r\n")[1].split("\n\r\n\r\n\x00")[1])
        print("___json",json[0].split(':'))
        self.debug(reply)
        print("final result:",res)
        return res
    def sendHTTPRequest_POST(self,ser,host,request):
        ''' send function'''
        data = {'id':self.id,'longitude' :self.current_long,'latitude'  :self.current_lat,'speed':self.speed,'time':self.time}
        content=JSON.dumps(data)
        ser.write(str.encode('AT+CIPSEND'+'\r\n'))
        time.sleep(2)
        request =str.encode(write_request(content,host.split('"')[1],"POST",request)+ "\r\n\r\n")
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
