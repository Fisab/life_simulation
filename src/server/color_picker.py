import json


class ColorPicker:
	def __init__(self, config_name='config.json'):
		self.__config_name = config_name
		self.__colors = self.__load_config()

		self.EMPTY = -1

	def __load_config(self):
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
		return list(range(len(self.__colors['INDEX_BLOCKS'])))

	def get_color_by_name(self, name):
		return tuple(self.__colors[name])

	def get_name_by_id(self, id):
		return self.__colors['INDEX_BLOCKS'][id]
