import gen_map
from PIL import Image, ImageDraw
import time
import helpers

generator = gen_map.MapGenerator(size_x=1000, size_y=1000)

cells = generator.generate_map(return_map=True)

cell_size = 16
cell_amount = generator.get_map_size()

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
		draw.rectangle(xy, fill=helpers.blend(cells[y][x]))

draw_grid(draw)

img.save('map.jpg')

print('Time spent for draw and save img -', time.time() - s_time)