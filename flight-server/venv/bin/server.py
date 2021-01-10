from flask import Flask, jsonify
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

@app.route('/api/time')
def get_current_time():
    return {'time': datetime.datetime.now()}

@app.route('/api/params', methods = ['POST'])
def get_flight_params():
    dropHeight = request.args.get(dropHeight)
    dropColumns = request.args.get(dropColumns)
    dropRows = request.args.get(dropRows)
    return jsonify(dropHeight=dropHeight, dropColumns=dropColumns, dropRows=dropRows)
    