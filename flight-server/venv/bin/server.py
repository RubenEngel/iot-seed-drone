from flask import Flask
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}