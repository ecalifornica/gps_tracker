from datetime import datetime

from flask import Flask, request, render_template
import pymongo

app = Flask(__name__)
mc = pymongo.MongoClient()
db = mc.gps_test
collection = db.test_col


@app.route('/gps', methods=['GET', 'POST'])
def coordinate_upload():
    if request.method == 'GET':
        return 'hello world'
    if request.method == 'POST':
        # print request.data
        data = request.json
        gps_points = []
        for i in data:
            lon = float(data[i][1].rstrip())
            lat = float(data[i][0])
            # Use another NMEA sentence
            pt_date = datetime.utcnow().date()
            pt_time = datetime.strptime(i, '%H:%M:%S').time()
            ts = datetime.combine(pt_date, pt_time)
            doc = {'timestamp': ts, 'coord': [lon, lat]}
            print(doc)
            gps_points.append(doc)
        collection.insert_many(gps_points)
        return 'accepted'


@app.route('/track')
def track():
    db_result = (collection
                 .find()
                 .sort('timestamp', pymongo.DESCENDING)
                 .limit(360))
    coords = []
    for i in db_result:
        print(i)
        if i['coord'] == [0.0, 0.0]:
            continue
        coords.append(i['coord'])
    return render_template('track.html', coords=coords)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
