from utils import *
import math

sample_name = "mahmud"

Utils.make_cropped_grayscale_image(sample_name)

pins_count = 200

pins = []

degree = -math.radians(360 / pins_count)

for i in range(pins_count):
    pin = [
        500 - (round(math.sin(degree * i) * 500)),
        500 - (round(math.cos(degree * i) * 500))
    ]
    pins.append(pin)

# print(pins)

img = Image.open(f"result/r_{sample_name}.png").convert("RGB")
img_matrix = np.asarray(img)

for i in pins:
    img_matrix[min(i[0], 999)][min(i[1], 999)] = [255, 0, 0]

tst = Image.fromarray(img_matrix)

tst.save(f"result/rr_{sample_name}.png")
