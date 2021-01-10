from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
CORS(app, support_credentials=True)

@app.route('/api/time')
def get_current_time():
    return {'time': datetime.datetime.now()}

@app.route('/api/params', methods = ['POST'])
def get_flight_params():
    flight_params = request.get_json()
    dropHeight = flight_params['dropHeight']
    dropColumns = flight_params['dropColumns']
    dropRows = flight_params['dropRows']
    return dropHeight, dropColumns, dropRows


@app.route('/api/log')
def get_mission_log():
    missionLog = []
    dropHeight, dropColumns, dropRows = get_flight_params()
    missionLog.append('Flying to altitude of {}'.format(dropHeight))
    return jsonify({'missionLog' : missionLog})