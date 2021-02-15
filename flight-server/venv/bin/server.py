from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import datetime
import time
import subprocess
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, support_credentials=True)
socket = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

@app.route('/api/time')
def get_current_time():
    return {'time': datetime.datetime.now()}

###### GET FLIGHT PARAMETER FROM FRONT END SUBMISSION

drop_height = 0
drop_columns = 0
drop_rows = 0
drop_spacing = 0

@app.route('/api/params', methods = ['POST'])
def get_flight_params():
    flight_params = request.get_json()
    print(flight_params)
    global drop_height
    global drop_columns
    global drop_rows
    global drop_spacing
    drop_height = flight_params['dropHeight']
    drop_columns = flight_params['dropColumns']
    drop_rows = flight_params['dropRows']
    drop_spacing = flight_params['dropSpacing']
    return 'Done', 201

@socket.on('connect')
def on_connect():
    print('user connected')

@socket.on('flight-start')
def on_flight_start():
    emit('message', 'Flight parameters sent successfully.')
    process = subprocess.Popen(['stdbuf', '-o0', '/usr/bin/python', '/home/pi/iot-seed-drone/flight-server/flight-scripts/basic_mission.py', '--connect', '127.0.0.1:14550',\
    '--height', str(drop_height), '--spacing', str(drop_spacing), '--columns', str(drop_columns), '--rows', str(drop_rows) ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while process.poll() is None:
        for line in iter(process.stdout.readline, b''):
            emit('message', line.rstrip().decode('utf-8'))
    emit('message', 'Mission complete.')
    time.sleep(1)
    emit('status', 'complete')
    

if __name__ == '__main__':
    socket.run(app)
