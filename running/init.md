# summery ideal case:
1. create network name : `A` pass = `i12345678`
2. find ip with [__fing__](https://play.google.com/store/apps/details?id=com.overlook.android.fing
) at other phone app from other mobil or `ping raspberrypi.local`
3. connect with putty ssh `putty.exe --ssh pi@192.168.43.237 22`
or use gui ask @ siam
4. deactivate image enviroment `deactivate`
5. run  `python3 mainGsmGpsAcc.py`
__application links at bottom__

## connecting to rasbery 

create hostspot from mobile with config:
ssid = A
pass = i12345678

or use ethernet to add other network at `/etc/wpa_supplicant/wpa_supplicant.conf`

### ip of raspery:
try 'ssh pi@192.168.43.237'

- if flailed
> connect lab to same network and try to ping pi
'ping raspberrypi.local'
```
PING raspberrypi.local (192.168.1.131): 56 data bytes
64 bytes from 192.168.43.237: icmp_seq=0 ttl=255 time=2.618 ms
64 bytes from 192.168.43.237: icmp_seq=0 ttl=255 time=2.618 ms
```

if failed 
> open fing app from __OTHER__ phone connect in same network https://play.google.com/store/apps/details?id=com.overlook.android.fing

if no other phone available
> try angry ip scanner for windows https://angryip.org/download/#windows

if all above failed use ethernet cable 
- try them again with ethernet 
in pi run to get ip
>'ifconfig'


## runnning gps/gsm/acc code

```bash
deactivate
python3 mainGsmGpsAcc.py
```
### if gsm has problem
```
python3 hsp_no     -->> press tap to complate file name which will use wifi network to send data
```
make sure mobile has internet connection


### open server ot view sent data 
http://evilcar.herokuapp.com/obstacles/json
or for violation data
http://evilcar.herokuapp.com/

you may call me just __before presenting i will server with some data

## you can view camera result at
https://youtu.be/3U70DeE1qAc

i can not run it in pi because it uses gpu for processing


### u may need download
https://angryip.org/download/#windows
https://play.google.com/store/apps/details?id=com.overlook.android.fing
https://www.putty.org/
