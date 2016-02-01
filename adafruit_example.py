import gps
import time

session = gps.gps('localhost', '8888')
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    try:
        report = session.next()
        #print(dir(report))
        #print(report.keys())
        if report['class'] == 'TPV':
            if hasattr(report, 'time'):
                print(report.time, report.lat, report.lon)
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print('GPSD has terminated')
