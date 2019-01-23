import gen_map
from PIL import Image, ImageDraw
import time
import helpers
import color_picker

generator = gen_map.MapGenerator(size_x=10000, size_y=10000)
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


img = Image.new('RGB', map_surface_size)
draw = ImageDraw.Draw(img)

s_time = time.time()

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

draw_grid(draw)

img.save('../../imgs/map_example.jpg')

print('Time spent for draw and save img -', time.time() - s_time)