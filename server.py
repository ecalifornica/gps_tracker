from flask import Flask, request
import pymongo

app = Flask(__name__)

@app.route('/gps', methods=['GET', 'POST'])
def hi():
    if request.method == 'POST':
        # print request.data
        print request.json

        return 'accepted'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
