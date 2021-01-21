from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import datetime
import time
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, support_credentials=True)
socket = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

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

# @app.route('/api/open', methods = ['POST'])
# def open_motor():
#     subprocess.call(['python', 'open.py'])

# @app.route('/api/close', methods = ['POST'])
# def close_motor():
#     subprocess.call(['python', 'close.py'])

@socket.on('connect')
def on_connect():
    print('user connected')

@socket.on('flight-start')
def on_flight_start():
    emit('message', 'Flying to altitude: {}m..'.format(dropHeight))
    time.sleep(int(dropHeight))
    emit('message', 'Altitude reached.')
    time.sleep(1)
    subprocess.call(['python', 'open.py'])
    emit('message', 'Dropping seeds..')
    time.sleep(3)
    subprocess.call(['python', 'close.py'])
    emit('message', 'Flying to next way point {}m away..'.format(dropSpacing))
    time.sleep(int(dropSpacing))
    emit('message', 'Destination reached.')
    time.sleep(1)
    subprocess.call(['python', 'open.py'])
    emit('message', 'Dropping seeds..')
    time.sleep(3)
    subprocess.call(['python', 'close.py'])
    emit('message', 'Mission complete.')
    time.sleep(3)
    emit('status', 'complete')
    

if __name__ == '__main__':
    socket.run(app)