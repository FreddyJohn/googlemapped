import pynmea2
import serial
def getPosition():
        port="/dev/ttyACM0"
        ser=serial.Serial(port, baudrate=9600, timeout=0.5)
        while True:
                dataout = pynmea2.NMEAStreamReader()
                newdata=ser.readline()
                newdata=newdata.decode('utf-8').replace("\\r\\n",'')
                if newdata[0:6] == "$GPRMC":
                        newmsg=pynmea2.parse(newdata)
                        lat=newmsg.latitude
                        lng=newmsg.longitude
                        #gps = str(lat) + "  ,  " + str(lng)
                        return [str(lat),str(lng)]

#port="/dev/ttyACM0"
#ser=serial.Serial(port, baudrate=9600, timeout=0.5)
def getTableNameFrom(position):
    latlng_block=""
    if position[0].find("-")==0 and position[1].find("-")!=0:
        latlng_block=position[0][:6]+"_"+position[1][:5]
    elif position[1].find("-")==0 and position[0].find("-")!=0:
        latlng_block=position[0][:5]+"_"+position[1][:6]
    else:
        latlng_block=position[0][:5]+"_"+position[1][:5]
    return latlng_block
