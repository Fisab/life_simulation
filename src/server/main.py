import threading
from flask import Flask
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
	print('sdf')

	return 'Hello world!'


@socketio.on('connect')
def handle_message(message):
	print('received connect: ' + message)


@socketio.on('message')
def handle_message_(message):
	print('received message: ' + message)


if __name__ == '__main__':
	socketio.run(app, host='localhost', port=10001)
