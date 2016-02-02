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
            doc = {'timestamp': i, 'coord': [lon, lat]}
            print(doc)
            gps_points.append(doc)
        mc_result = collection.insert_many(gps_points)
        #print(dir(mc_result))
        print(mc_result.inserted_ids)
        
        return 'accepted'


@app.route('/track')
def track():
    return render_template('track.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
