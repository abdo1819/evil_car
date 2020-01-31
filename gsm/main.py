from gsm import gsm

g = gsm()
g.isready(g.ser)
g.connectgsm(g.ser,g.apn)
g.connectTCP(g.ser,g.host,80)
g.sendHTTPRequest(g.ser,g.host,g.request)