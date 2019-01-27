import gen_map
from PIL import Image, ImageDraw
import time
import color_picker

generator = gen_map.MapGenerator(size_x=1000, size_y=1000)
color_pick = color_picker.ColorPicker()

s_time_gen_world = time.time()

generator.generate_world()

print('Time spent for generating world -', time.time() - s_time_gen_world)

cells = generator.get_world_type_blocks()
cells_height = generator.get_world_height()

cell_size = 4
cell_amount = generator.get_world_size()

map_surface_size = (
	cell_amount['x'] * cell_size,
	cell_amount['y'] * cell_size
)

grid_color = '#3C3F41'


def draw_grid(draw_obj):
	for y in range(cell_amount['y']+1):
		pos = [
			y * cell_size,
			0,
			y * cell_size,
			map_surface_size[1]
		]
		draw_obj.line(pos, fill=grid_color)

	for x in range(cell_amount['x']+1):
		pos = [
			0,
			x * cell_size,
			map_surface_size[0],
			x * cell_size
		]
		draw_obj.line(pos, fill=grid_color)


def draw_map(cells, draw):
	for y, _ in enumerate(cells):
		for x, _ in enumerate(cells[y]):
			xy = [
				x * cell_size,
				y * cell_size,
				x * cell_size + cell_size,
				y * cell_size + cell_size
			]
			if cells[y][x] != color_pick.EMPTY:
				color = color_pick.get_color_by_id(int(cells[y][x]))

				if color_pick.get_name_by_id(int(cells[y][x])) == 'WATER':  # shade dependence on height
					color = (
						color[0],
						int(color[1] + cells_height[y][x] * 250),
						color[2]
					)
				draw.rectangle(xy, fill=color)
			else:
				# draw.rectangle(xy, fill=helpers.blend(cells_height[y][x]))
				draw.rectangle(xy, fill=(0, 0, 0))


def process(imgs_count=1):
	global cells

	av_time_ep = []
	for i in range(imgs_count):
		s_time_ep = time.time()

		img = Image.new('RGB', map_surface_size)
		draw = ImageDraw.Draw(img)

		draw_map(cells, draw)
		draw_grid(draw)

		generator.process_weather()
		cells = generator.get_world_type_blocks()

		if len(str(i)) == 1:
			i = '00' + str(i)
		elif len(str(i)) == 2:
			i = '0' + str(i)

		img.save('../../imgs/map_example_%s.jpg' % str(i))

		av_time_ep.append(time.time() - s_time_ep)

	print('Average time spent for process and save 1 episode -', sum(av_time_ep) / len(av_time_ep))


if __name__ == '__main__':
	s_time = time.time()

	process()

	print('Time spent for draw and save images -', time.time() - s_time)