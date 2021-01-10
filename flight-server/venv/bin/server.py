from flask import Flask
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

@app.route('/api/time')
def get_current_time():
    return {'time': datetime.datetime.now()}