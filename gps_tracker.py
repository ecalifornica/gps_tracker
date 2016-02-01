import serial
import time

import pynmea2


def read_gps():
    gps_conn = serial.Serial('/dev/ttyO4', 9600)
    while True:
        data = gps_conn.readline()
        if data.startswith('$GPGGA'):
            msg = pynmea2.parse(data)
            # GPS.reset_input_buffer()
            return msg.timestamp, msg.latitude, msg.longitude
    gps_conn.close()


if __name__ == '__main__':
    while True:
        ts, lat, lon = read_gps()
        with open('/var/tmp/gps_track.txt', 'a+') as file_handle:
            print(ts.isoformat(), lat, lon)
            file_handle.write('{}, {}, {}\n'.format(ts.isoformat(), lat, lon))
        time.sleep(9)
