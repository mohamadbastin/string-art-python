from copy import copy
from random import random
from re import A
import time
from utils import *
import math
from PIL import Image, ImageDraw, ImageOps, ImageFilter

sample_name = "mahmud"
number_of_lines = 3000

Utils.make_cropped_grayscale_image(sample_name)

blured_original = Image.open(f"result/r_b_{sample_name}.png")
blured_original_array = np.array(blured_original)

pins_count = 200

pins = Utils.get_pins(pins_count)

empty_board = Utils.create_board(pins)

pins_order = [pins[0]]


def is_allowed(prev, nxt):
    if prev == nxt:
        return False

    for i in range(len(pins_order)):
        try:
            if pins_order[i] == prev and pins_order[i + 1] == nxt:
                return False
            elif pins_order[i] == nxt and pins_order[i + 1] == prev:
                return False
        except:
            pass

    return True


def compute_cost(pins_order, next_pin):
    board = copy(empty_board)
    new_order = copy(pins_order)
    new_order.append(next_pin)
    blured_board_array = Utils.get_blured_new_board(board, new_order)
    s = 0.00
    for h in range(1000):
        for w in range(1000):
            # print(int(blured_board_array[h][w][0]))
            # print(int(blured_original_array[h][w]))
            diff = (int(blured_board_array[h][w][0]) -
                    int(blured_original_array[h][w]))**2  #TODO scale to 0-1

            s += diff

    return s / 1e6


main_board = copy(empty_board)
draw = ImageDraw.Draw(main_board)

for i in range(number_of_lines):
    start = time.time()
    best_cost = math.inf
    best_next_pin = None
    previous_pin = pins_order[-1]

    if (len(pins_order) > 1):
        Utils.draw_line(draw, pins_order[-2], pins_order[-1])
        Utils.save_board(main_board)
    # print(i, pins_order)
    print(len(pins_order) - 1)
    for next_pin in pins:

        if is_allowed(previous_pin, next_pin):
            cost = compute_cost(pins_order, next_pin)
            if cost < best_cost:
                best_cost = cost
                best_next_pin = next_pin

    if best_next_pin == None:
        break
    end = time.time()
    print(cost, best_next_pin, end - start)
    pins_order.append(best_next_pin)

# main_board = copy(empty_board)
# draw = ImageDraw.Draw(main_board)

for i in range(len(pins_order) - 1):
    Utils.draw_line(draw, pins_order[i], pins_order[i + 1])

Utils.save_board(main_board)

print("done")
