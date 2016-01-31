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
    # print NMEA
    if barf[:6] == '$GPGGA':
        with open('/var/tmp/gps_track.txt', 'a') as fh:
            msg = pynmea2.parse(barf)
            print(msg.latitude, msg.longitude)
            # print(help(msg))
            #fh.write(pickle.dumps(msg))
            pickle.dump(msg, fh)


while True:
    read_gps()
