from utils import *
import math

sample_name = "mahmud"
number_of_lines = 3000

Utils.make_cropped_grayscale_image(sample_name)

pins_count = 4

pins = Utils.get_pins(pins_count)

board = Utils.create_board(pins)

draw = ImageDraw.Draw(board)

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


def compute_cost(pins_order, previous_pin, next_pin):
    pass


for i in range(number_of_lines):
    best_cost = math.inf
    best_next_pin = None
    previous_pin = pins_order[-1]

    for next_pin in pins:
        if is_allowed(previous_pin, next_pin):
            cost = compute_cost(pins_order, previous_pin, next_pin)
            if cost < best_cost:
                best_cost = cost
                best_next_pin = next_pin

    if best_next_pin == None:
        break

    pins_order.append(best_next_pin)

print("done")