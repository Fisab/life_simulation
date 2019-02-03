import time
import numpy as np


def log(*argv):
	"""
	Maybe someday i make normal logging...
	:return:
	"""
	msg = ''
	for i in argv:
		msg += i + ' '
	print(msg)


def blend(alpha, base=(255, 255, 255), color=(0, 0, 0)):
	"""
	:param color should be a 3-element iterable,  elements in [0,255]
	:param alpha should be a float in [0,1]
	:param base should be a 3-element iterable, elements in [0,255] (defaults to white)

	:return: rgb, example: (255, 255, 255)
	"""

	return tuple(int(round((alpha * color[i]) + ((1 - alpha) * base[i]))) for i in range(3))


def sleep(sec):
	time.sleep(sec)


def get_part_array(array, part, additional_area, offset={'x': 0, 'y': 0}):
	"""
	Retrieve part of array
	:param array: supposed for world
	:param part: size of x and y
	:param offset: offset for world
	:return: part of world
	"""
	result = []

	offset_before = {
		'x': offset['x'] - additional_area['x'],
		'y': offset['y'] - additional_area['y']
	}
	if offset_before['x'] < 0:
		print('set x')
		offset_before['x'] = 0
	if offset_before['y'] < 0:
		print('set y')
		offset_before['y'] = 0

	for i in array[offset_before['y'] : offset['y']+part['y']+additional_area['y']]:
		result.append(i[offset_before['x'] : offset['x']+part['x']+additional_area['x']])
	return np.array(result)
