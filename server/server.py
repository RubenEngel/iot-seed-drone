from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
io = SocketIO(app)

@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    io.run(app, host="0.0.0.0", port=5000)
