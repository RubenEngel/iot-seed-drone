from flask import Flask, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, support_credentials=True)

@app.route('/api/time')
def get_current_time():
    return {'time': datetime.datetime.now()}

@app.route('/api/params', methods = ['POST'])
def get_flight_params():
    dropHeight = request.args.get('dropHeight')
    dropColumns = request.args.get('dropColumns')
    dropRows = request.args.get('dropRows')
    return 'Done', 201
    
@app.route('/api/log')
def get_mission_log():
    missionLog = ['Test1' 'Test2' 'Test3']
    return jsonify({'missionLog' : missionLog})