import time
import noise
import random
import pickle
import os
import numpy as np
import helpers
import color_picker


class MapGenerator:
	def __init__(self, size_x=1000, size_y=1000):
		self.__hashed_map = []
		# hashed_map contains all episode's after start simulation
		# 0 - contains first map state
		# 1 - second
		# etc...

		self.__world_size = {
			'x': size_x,
			'y': size_y
		}

		self.__world_type_blocks = []

		self.__world_height = []
		self.__world_temp = [] # temperature

		self.__seed_height = random.random()
		self.__seed_temp = random.random()

		self.__scale = 0.015

		self.__color_pick = color_picker.ColorPicker()

	def get_dist_nearest_block(self, cur_pos, radius_lookup=5):
		"""
		Find any nearest block which equal for block_id.
		Finding block from pos - cur_pos
		:param block_id: example: 0
		:param cur_pos: example: {'x': 12, 'y': 12}
		:return: distance to any block with same block_id, float
		"""
		nearest_block_pos = {
			self.__color_pick.get_name_by_id(i): None for i in self.__color_pick.get_available_ids()
		}

		for radius in range(1, radius_lookup):
			for i in range(cur_pos['x'] - radius, cur_pos['x'] + radius + 1):
				if cur_pos['y'] - radius < 0 or \
					cur_pos['y'] + radius >= self.__world_size['y'] - 1 or \
					i > self.__world_size['x'] - 1 or \
					i < 0:
					continue

				if self.__world_type_blocks[cur_pos['y'] - radius][i] != self.__color_pick.EMPTY:
					block_id = self.__world_type_blocks[cur_pos['y'] - radius][i]
					block_name = self.__color_pick.get_name_by_id(block_id)
					if nearest_block_pos[block_name] is None:
						nearest_block_pos[block_name] = {
							'x': i,
							'y': cur_pos['y'] - radius
						}

				if self.__world_type_blocks[cur_pos['y'] + radius][i] != self.__color_pick.EMPTY:
					block_id = self.__world_type_blocks[cur_pos['y'] + radius][i]
					block_name = self.__color_pick.get_name_by_id(block_id)
					if nearest_block_pos[block_name] is None:
						nearest_block_pos[block_name] = {
							'x': i,
							'y': cur_pos['y'] + radius
						}

			for i in range(cur_pos['y'] - radius, cur_pos['y'] + radius + 1):
				if cur_pos['x'] - radius < 0 or \
					cur_pos['x'] + radius >= self.__world_size['x'] - 1 or \
					i > self.__world_size['y'] - 1 or \
					i < 0:
					continue

				if self.__world_type_blocks[i][cur_pos['x'] - radius] != self.__color_pick.EMPTY:
					block_id = self.__world_type_blocks[i][cur_pos['x'] - radius]
					block_name = self.__color_pick.get_name_by_id(block_id)
					if nearest_block_pos[block_name] is None:
						nearest_block_pos[block_name] = {
							'x': i,
							'y': cur_pos['x'] - radius
						}

				if self.__world_type_blocks[i][cur_pos['x'] + radius] != self.__color_pick.EMPTY:
					block_id = self.__world_type_blocks[i][cur_pos['x'] + radius]
					block_name = self.__color_pick.get_name_by_id(block_id)
					if nearest_block_pos[block_name] is None:
						nearest_block_pos[block_name] = {
							'x': i,
							'y': cur_pos['x'] + radius
						}

		for block_name in nearest_block_pos:
			if nearest_block_pos[block_name] is None:
				continue
			nearest_block_pos[block_name] = (
				(nearest_block_pos[block_name]['x'] - cur_pos['x'])**2 +
				(nearest_block_pos[block_name]['y'] - cur_pos['y'])**2
			)**0.5

		return nearest_block_pos

	def generate_world(self):
		helpers.log('Generating map...')

		self.__world_height = np.zeros((self.__world_size['x'], self.__world_size['y']))
		self.__world_temp = np.zeros((self.__world_size['x'], self.__world_size['y']))
		self.__world_type_blocks = np.ones((self.__world_size['x'], self.__world_size['y'])) * -1

		helpers.log('\t-| Generating noise, placing water and mountains...')
		for y in range(self.__world_size['x']):
			for x in range(self.__world_size['y']):
				# gen noise
				height = noise.pnoise3(
					float(x) * self.__scale,
					float(y) * self.__scale,
					self.__seed_height,
					1
				)
				temp = noise.pnoise3(
					float(x) * self.__scale,
					float(y) * self.__scale,
					self.__seed_temp,
					1
				)

				self.__world_height[y][x] = height
				self.__world_temp[y][x] = temp

				# place water...
				if height < -0.15:
					if temp < -0.2:
						self.__world_type_blocks[y][x] = self.__color_pick.get_id_by_name('ICE')
					else:
						self.__world_type_blocks[y][x] = self.__color_pick.get_id_by_name('WATER')

				# place mountains...
				if height > 0.5:
					if temp < 0.45:
						self.__world_type_blocks[y][x] = self.__color_pick.get_id_by_name('SNOW_MOUNTAIN')
					else:
						self.__world_type_blocks[y][x] = self.__color_pick.get_id_by_name('MOUNTAIN')

		helpers.log('\t-| Placing sand, snow, land, grass...')
		for y in range(self.__world_size['x']):
			for x in range(self.__world_size['y']):
				if self.__world_type_blocks[y][x] != self.__color_pick.EMPTY:
					continue

				# At part below for place snow and sand i try find nearest blocks(water, ice), but it too slow.
				# Seems without this world look pretty too
				# Maybe i will have an idea how optimize this, or, or just delete :P
				# cur_pos = {
				# 	'x': x,
				# 	'y': y
				# }
				# distance_blocks = self.get_dist_nearest_block(cur_pos, radius_lookup=10)

				# place snow
				# if distance_blocks['SNOW'] is not None and distance_blocks['SNOW'] < 1:
				# 	self.__world_type_blocks[y][x] = self.__color_pick.get_id_by_name('SNOW')
				# else:
				# 	# place sand...
				# 	if distance_blocks['WATER'] is not None and distance_blocks['WATER'] < 8:
				# 		self.__world_type_blocks[y][x] = self.__color_pick.get_id_by_name('SAND')
				# if self.__world_type_blocks[y][x] != self.__color_pick.EMPTY:
				# 	continue

				# place land, grass, snow, sand
				if self.__world_temp[y][x] > 0.5:
					self.__world_type_blocks[y][x] = self.__color_pick.get_id_by_name('SAND')
				elif self.__world_temp[y][x] < -0.15:
					self.__world_type_blocks[y][x] = self.__color_pick.get_id_by_name('SNOW')
				else:
					if self.__world_temp[y][x] > 0.1:
						self.__world_type_blocks[y][x] = self.__color_pick.get_id_by_name('GRASS')
					else:
						self.__world_type_blocks[y][x] = self.__color_pick.get_id_by_name('LAND')

	def get_world_height(self):
		return self.__world_height

	def get_world_type_blocks(self):
		return self.__world_type_blocks

	def get_world_size(self):
		return self.__world_size

	def append_hashed_world(self, world):
		self.__hashed_map.append(world)

	@staticmethod
	def __save_file(file_name, data):
		"""
		Save data any obj to pickle file
		:param file_name: name of file
		:param data: data to be saved into file
		:return: None
		"""
		try:
			with open(file_name, 'wb') as f:
				pickle.dump(data, f)
		except Exception as e:
			helpers.log('Got some error while saving file: "%s"\nfile_name: %s' % (e, file_name))

	@staticmethod
	def __load_file(file_name):
		"""
		Load pickle file and return data
		:param file_name: name of loading file
		:return: file data
		"""
		if os.path.exists(file_name):
			try:
				with open(file_name, 'rb') as f:
					return pickle.load(f)
			except Exception as e:
				helpers.log('Got some error while reading file: "%s"\nfile_name: %s' % (e, file_name))
		else:
			helpers.log('File with name "%s" do not exist\'s' % file_name)

	def save_episodes(self, file_name='episodes.pkl'):
		self.__save_file(file_name, self.__hashed_map)

	def save_world_type_blocks(self, file_name='world.pkl'):
		self.__save_file(file_name, self.__world_type_blocks)

	def load_episodes(self, file_name='episodes.pkl'):
		self.__hashed_map = self.__load_file(file_name)

	def load_world(self, file_name='world.pkl'):
		self.__world_type_blocks = self.__load_file(file_name)


if __name__ == '__main__':
	generator = MapGenerator()

	time_eps = []
	s_time_all = time.time()
	for _ in range(10):
		s_time_ep = time.time()
		generator.generate_world()
		generator.append_hashed_world(generator.get_world_type_blocks())
		time_eps.append(time.time() - s_time_ep)

	print('Spent time for all episodes generating map -', time.time() - s_time_all)
	print('Spent mean time for each episode generating map -', sum(time_eps)/len(time_eps))

	time_saving = time.time()
	generator.save_episodes()
	print('Spent time for saving all 100 episodes -', time.time() - time_saving)

	time_loading = time.time()
	generator.load_episodes()
	print('Spent time for loading all 100 episodes -', time.time() - time_loading)

