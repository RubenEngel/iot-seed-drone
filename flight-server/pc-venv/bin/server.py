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

@app.route('/api/params', methods = ['POST']) # when post method received on api route
def get_flight_params(): # complete the following function
    flight_params = request.get_json() # get json object of flight parameters
    global drop_height # use global variable in this function
    global drop_columns # use global variable in this function
    global drop_rows # use global variable in this function
    global drop_spacing # use global variable in this function
    drop_height = flight_params['dropHeight'] # set drop height to the number received from front end
    drop_columns = flight_params['dropColumns'] # set drop columns to the number received from front end
    drop_rows = flight_params['dropRows'] # set drop rows to the number received from front end
    drop_spacing = flight_params['dropSpacing'] # set drop spacing to the number received from front end
    return 'Done', 201 # send status code back to front end

@socket.on('connect') # when user connect to socket
def on_connect():
    print('user connected')

@socket.on('flight-start') # when flight start command received from socket
def on_flight_start():
    emit('message', 'Flight parameters sent successfully.')
    process = subprocess.Popen(['stdbuf', '-o0', '/usr/bin/python', '/home/dronedojo/iot-seed-drone/flight-server/flight-scripts/basic_mission.py', '--connect', '127.0.0.1:14550',\
    '--height', str(drop_height), '--spacing', str(drop_spacing), '--columns', str(drop_columns), '--rows', str(drop_rows) ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while process.poll() is None: # while process is running
        for line in iter(process.stdout.readline, b''):
            print(line.rstrip().decode('utf-8'))
            emit('message', line.rstrip().decode('utf-8'))
    emit('message', 'Mission complete.')
    time.sleep(1)
    emit('status', 'complete')
    

if __name__ == '__main__':
    socket.run(app)