import pickle
import serial
import time

import Adafruit_BBIO.UART as UART
import pynmea2
#UART.setup("UART4")
GPS = serial.Serial('/dev/ttyO4', 9600)


def read_gps():
    while GPS.inWaiting()==0:
        pass
    barf=GPS.readline()
    print barf
    if barf[:6] == '$GPGGA':
        with open('/var/tmp/gps_track.txt', 'a') as fh:
            msg = pynmea2.parse(barf)
            print(msg.latitude, msg.longitude)
            # print(help(msg))
            #fh.write(pickle.dumps(msg))
            pickle.dump(msg, fh)

def read_gps_2():
    GPS.reset_input_buffer()
    while True:
        data = GPS.readline()
        if data.startswith("$GPGGA"):
            msg = pynmea2.parse(data)
            #print(repr(msg))
            #print(dir(msg))
            #print(msg.data, msg.fields)
            #GPS.reset_input_buffer()
            #GPS.flushOutput()
            return msg.timestamp, msg.latitude, msg.longitude

while True:
    result = read_gps_2()
    print(result[0].isoformat(), result[1], result[2])
    time.sleep(5)

