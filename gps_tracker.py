import json
import serial
import time

import pynmea2
import requests

import config


def read_gps():
    gps_conn = serial.Serial('/dev/ttyO4', 9600)
    while True:
        # gps_conn.reset_input_buffer()
        data = gps_conn.readline()
        if data.startswith('$GPGGA'):
            msg = pynmea2.parse(data)
            return msg.timestamp, msg.latitude, msg.longitude
    gps_conn.close()


def upload_track():
    with open('/var/tmp/gps_track.txt', 'r') as fh:
        payload = {}
        for line in fh:
            data = line.split(',')
            payload[data[0]] = [data[1], data[2]]
    with open('/var/tmp/gps_track.txt', 'w') as fh:
        pass
    r = requests.post(config.API_URL, json=payload)
    


if __name__ == '__main__':
    last_upload = time.time()
    while True:
        ts, lat, lon = read_gps()
        with open('/var/tmp/gps_track.txt', 'a+') as fh:
            #print(ts.isoformat(), lat, lon)
            fh.write('{},{},{}\n'.format(ts.isoformat(), lat, lon))
        if time.time() - last_upload > 60:
            upload_track()
            last_upload = time.time()
        time.sleep(9)
