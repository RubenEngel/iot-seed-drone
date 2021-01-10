from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import datetime
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
CORS(app, support_credentials=True)

@app.route('/api/time')
def get_current_time():
    return {'time': datetime.datetime.now()}

###### GET FLIGHT PARAMETER FROM FRONT END SUBMISSION

dropHeight = 0
dropColumns = 0
dropRows = 0
dropSpacing = 0

@app.route('/api/params', methods = ['POST'])
def get_flight_params():
    flight_params = request.get_json()
    print(flight_params)
    global dropHeight
    global dropColumns
    global dropRows
    global dropSpacing
    dropHeight = flight_params['dropHeight']
    dropColumns = flight_params['dropColumns']
    dropRows = flight_params['dropRows']
    dropSpacing = flight_params['dropSpacing']
    return 'Done', 201

missionLog = []
# missionLog.append('Total drop rows = {}'.format(dropRows))
# missionLog.append('Total drop columns = {}'.format(dropColumns))
# missionLog.append('Flying to altitude of {}'.format(dropHeight))
# missionLog.append('Reached target altitude')
# missionLog.append('Dropping Seeds')
# missionLog.append('Moving {}m, to next waypoint..'.format(dropSpacing))


##### GET MISSION LOG   

@app.route('/api/log')
def get_mission_log():
    global missionLog
    missionLog.append('Total drop rows = {}'.format(dropRows))
    missionLog.append('Total drop columns = {}'.format(dropColumns))
    missionLog.append('Flying to altitude of {}'.format(dropHeight))
    missionLog.append('Reached target altitude')
    missionLog.append('Dropping Seeds')
    missionLog.append('Moving {}m, to next waypoint..'.format(dropSpacing))
    return jsonify({'missionLog' : missionLog})