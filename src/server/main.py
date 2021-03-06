from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from color_picker import ColorPicker
from gen_map import MapGenerator
import helpers

app = Flask(__name__, template_folder='../client')
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app)

colorPicker = ColorPicker()

map_size = {
	'x': 1000,
	'y': 500
}

generator = MapGenerator(size_x=map_size['x'], size_y=map_size['y'])

generator.generate_world()
cells = generator.get_world_type_blocks()


@app.route('/')
def index():
	print('Someone recieve main index')
	return render_template('index.html')


@app.route('/get_world')
def get_world():
	size_need = {
		'x': int(float(request.args.get('x'))),
		'y': int(float(request.args.get('y')))
	}
	offset_need = {
		'x': int(float(request.args.get('offset_x'))),
		'y': int(float(request.args.get('offset_y')))
	}
	additional_area = {
		'x': int(float(request.args.get('additional_area_x'))),
		'y': int(float(request.args.get('additional_area_y')))
	}

	part = helpers.get_part_array(cells, size_need, additional_area, offset_need)
	print(part.shape)
	return jsonify(part.tolist())


@app.route('/get_settings')
def get_settings():
	print('Someone retrieve palette')
	settings = colorPicker.get_config()
	settings['map_size'] = map_size

	return jsonify(settings)


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
