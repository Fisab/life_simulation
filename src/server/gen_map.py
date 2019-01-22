import time
import noise
import random
import pickle
import os
import numpy as np
import helpers


class MapGenerator:
	def __init__(self, size_x=1000, size_y=1000):
		self.__hashed_map = []
		# hashed_map contains all episode's after start simulation
		# 0 - contains first map state
		# 1 - second
		# etc...

		self.__map_size = {
			'x': size_x,
			'y': size_y
		}

		self.__map = []

		self.__seed = random.random()
		self.__scale = 0.025

	def generate_map(self, return_map=False):
		# gen empty list
		# world = np.zeros((self.__map_size['x'], self.__map_size['y']))
		world = []
		for y in range(self.__map_size['y']):
			world.append([[0, -1]] * self.__map_size['x'])  # height, type of block

		# gen noise
		for y in range(self.__map_size['x']):
			for x in range(self.__map_size['y']):
				world[y][x] = [
					noise.pnoise3(
						float(x) * self.__scale,
						float(y) * self.__scale,
						self.__seed,
						1
					),
					-1
				]

		# place water...
		for y in range(self.__map_size['x']):
			for x in range(self.__map_size['y']):
				if world[y][x][0] < 0:
					world[y][x] = [world[y][x][0], 0]
		#

		if return_map is True:
			return world
		else:
			self.__map = world

	def generate_empty_map(self, size_x=None, size_y=None, return_map=False):
		"""
		Just generate simple 2D array with '0'

		:This function will clear self.__map if return_map is False

		:param size_x: size map at axis x if it's None value get from init
		:param size_y: size map at axis y if it's None value get from init
		:return: None
		"""
		if size_x is None:
			size_x = self.__map_size['x']
		if size_y is None:
			size_y = self.__map_size['y']

		map = []
		for x in range(size_y):
			if return_map is True:
				map.append([0] * size_x)
			else:
				self.__map.append([0] * size_x)

		if return_map is True:
			return map

	def get_map(self):
		return self.__map

	def get_map_size(self):
		return  self.__map_size

	def append_hashed_map(self, map):
		self.__hashed_map.append(map)

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

	def save_map(self, file_name='map.pkl'):
		self.__save_file(file_name, self.__map)

	def load_episodes(self, file_name='episodes.pkl'):
		self.__hashed_map = self.__load_file(file_name)

	def load_map(self, file_name='map.pkl'):
		self.__map = self.__load_file(file_name)


if __name__ == '__main__':
	generator = MapGenerator()

	time_eps = []
	s_time_all = time.time()
	for _ in range(100):
		s_time_ep = time.time()
		generator.append_hashed_map(generator.generate_empty_map(return_map=True))
		time_eps.append(time.time() - s_time_ep)

	print('Spent time for all episodes generating map -', time.time() - s_time_all)
	print('Spent mean time for each episode generating map -', sum(time_eps)/len(time_eps))

	time_saving = time.time()
	generator.save_episodes()
	print('Spent time for saving all 100 episodes -', time.time() - time_saving)

	time_loading = time.time()
	generator.load_episodes()
	print('Spent time for loading all 100 episodes -', time.time() - time_loading)

