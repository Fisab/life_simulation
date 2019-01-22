import json


class ColorPicker:
	"""
	This class supposed for work with config which contains block's info(color, ids, etc...)
	"""
	def __init__(self, config_name='config.json'):
		self.__config_name = config_name
		self.__colors = self.__load_config()

		self.EMPTY = -1

	def __load_config(self):
		"""
		load file with name equal `self.__config_name`
		:return: file data
		"""
		with open(self.__config_name) as f:
			return json.load(f)

	def get_color_by_id(self, id):
		"""
		:param id: int, example: 0
		:return: rgb color from config, example: (255, 255, 255)
		"""
		name = self.__colors['INDEX_BLOCKS'][id]
		return self.get_color_by_name(name)

	def get_available_ids(self):
		"""
		:return: all ids what saved into config
		"""
		return list(range(len(self.__colors['INDEX_BLOCKS'])))

	def get_color_by_name(self, name):
		"""
		:param name: block name, example: "WATER"
		:return: rgb color, example: (255, 255, 255)
		"""
		return tuple(self.__colors[name])

	def get_name_by_id(self, id):
		"""
		:param id: block id, emaple: 0
		:return: rgb color, example: (255, 255, 255)
		"""
		return self.__colors['INDEX_BLOCKS'][id]