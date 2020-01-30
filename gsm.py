# gsm module
import serial
import time

if __name__ == "__main__":
    verbose=True
    host='evilcar.herokuapp.com' # the URL of the server 
    request='/speed?lat=31.205753&long=29.924526'
    apn="internet.etisalat"
    port=80
    def debug(reply):
        if verbose :
            print('debug:---',reply)
    
    serial_port='/dev/ttyUSB0'
    ser=serial.Serial(serial_port, baudrate=115200, timeout=5)
    #check the GSM+GPRS module 
    ser.write(str.encode('AT'+'\r\n'))
    time.sleep(2)    
    reply=ser.readline()
    print(reply)  
    debug(reply)
    time.sleep(1)    

    # disconnect any existing wirless connection
    ser.write(str.encode('AT+CIPSHUT'+'\r\n'))
    time.sleep(2)
    reply=ser.read(ser.inWaiting())
    debug(reply)     
    time.sleep(1)

# set all current parameters to user defined profile
def isready(ser):
    ser.write(str.edncode('ATZ'+'\r\n'))
    time.sleep(2)
    reply=ser.read(ser.inWaiting())
    debug(reply)     
    time.sleep(1)
# start task and set apn user id , password
def connectgsm(ser,apn):
    ser.write("AT+CSTT="+ apn +'"",""'+str.encode('\r\n'))
    time.sleep(2)
    reply=ser.read(ser.inWaiting())
    debug(reply)     
    time.sleep(1)
    #bringing up network
    ser.write('AT+CIICR'+str.encode('\r\n'))
    time.sleep(2)
    reply=ser.read(ser.inWaiting())
    while reply!='OK' :
            reply=ser.read(ser.inWaiting())
    debug(reply)     
    time.sleep(1)

    # getting IP address
    ser.write('AT+CIFSR'+str.encode('\r\n'))
    time.sleep(3)
    reply=ser.read(ser.inWaiting())
    debug(reply)     
    time.sleep(1)
    # returning all messages from modem
    reply=ser.read(ser.inWaiting())
    debug(reply)     
    return reply

# connect to the tcp
def connectTCP(ser, host , port):
    ser.write('AT+CIPSTART="TCP"',+ host +","+str.encode(port)+str.encode('\r\n'))
    time.sleep(5)
    reply=ser.read(ser.inWaiting())
    while reply!='OK':
            reply=ser.read(ser.inWaiting())
    debug(reply)
    return reply     
    time.sleep(1)
# send function
def sendHTTPRequest(ser,host,request):
    ser.write('AT+CIPSEND'+'\r\n')
    time.sleep(2)
    request ="GET " + request +str.encode("HTTP/1.1\r\nHost:"+ host + "\r\n\r\n")
    ser.write(request + chr(26))
    time.sleep(2)
 # close TCP
def closeTCP(ser,showresponse=False):
    ser.write('AT+CIPCLOSE=1'+'\r\n')
    reply=ser.read(ser.inwaiting())
    if showresponse:
        print ("server response:\n" + reply[(reply.index("SEND OK") + 9):])
    time.sleep(2)        

# get IPStatus
def getIPstatus(ser):
    ser.write('AT+CIPSTATUS'+str.encode('\r\n'))
    time.sleep(1)
    reply=ser.read(ser.inWaiting())
    return reply                




