import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__, template_folder='../client')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
	print('Someone recieve main index')

	return render_template('index.html')


@socketio.on('connect')
def handle_connect():
	print('Hello!')


@socketio.on('message')
def handle_message(data):
	print('received message: ' + str(data))
	emit('message', data)


if __name__ == '__main__':
	socketio.run(app, port=10001)
