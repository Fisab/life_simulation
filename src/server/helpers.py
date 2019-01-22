

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
