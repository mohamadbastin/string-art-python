from utils import *
import math

sample_name = "mahmud"

Utils.make_cropped_grayscale_image(sample_name)

pins_count = 4

pins = Utils.get_pins(pins_count)

board = Utils.create_board(pins)

draw = ImageDraw.Draw(board)
