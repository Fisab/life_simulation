import threading
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from color_picker import ColorPicker
from gen_map import MapGenerator

app = Flask(__name__, template_folder='../client')
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app)

colorPicker = ColorPicker()
generator = MapGenerator(size_x=300, size_y=400)

generator.generate_world()
cells = generator.get_world_type_blocks()


@app.route('/')
def index():
	print('Someone recieve main index')
	return render_template('index.html')


@app.route('/get_world')
def get_world():
	size_need = {
		'x': int(request.args.get('x')),
		'y': int(request.args.get('y'))
	}
	print(size_need)

	print('Someone get map')
	world = []
	size = {
		'x': 20,
		'y': 20
	}

	return jsonify(cells.tolist())


@app.route('/get_settings')
def get_settings():
	print('Someone retrieve palette')
	return jsonify(colorPicker.get_config())


@app.route('/get_example_world')
def get_example_world():
	return jsonify(cells.tolist())
#####


@socketio.on('connect')
def handle_connect():
	print('Hello!')


@socketio.on('message')
def handle_message(data):
	print('received message: ' + str(data))
	while True:
		data['counter'] += 1
		emit('message', data)
		socketio.sleep(0.5)

		if data['counter'] >= 3:
			break


if __name__ == '__main__':
	socketio.run(app, port=10001, debug=True)
