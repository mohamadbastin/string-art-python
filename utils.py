import math

import numpy as np
from PIL import Image, ImageDraw, ImageOps


class Utils:
    @staticmethod
    def make_cropped_grayscale_image(sample_name: str):
        img = Image.open(f"assets/{sample_name}.jpg")

        w, h = img.size
        dif = abs(w - h)

        if w < h:
            if dif % 2 == 0:
                dif1, dif2 = dif / 2
            else:
                dif1 = math.ceil(dif / 2)
                dif2 = math.floor(dif / 2)
            h = w
            img_cropped = img.crop((0, dif1, h, dif1 + h))
        else:
            if dif % 2 == 0:
                dif1, dif2 = dif / 2
            else:
                dif1 = math.ceil(dif / 2)
                dif2 = math.floor(dif / 2)
            w = h

            img_cropped = img.crop((dif1, 0, dif1 + h, h))

        img_cropped.save(f"result/original_{sample_name}.png")

        size = (w, h)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice(((0, 0), (h, w)), 0, 360, fill=255, outline="white")

        img_arr = np.array(img_cropped, dtype='uint8')
        mask_arr = np.array(mask)
        final_img_arr = np.dstack((img_arr, mask_arr))

        result = Image.fromarray(final_img_arr)
        result.resize((1000, 1000)).save(f"result/original_{sample_name}.png")

        rgb_img = Image.open(f"result/original_{sample_name}.png").convert('L')
        rgb_img.save(f"result/original_{sample_name}.png")

    @staticmethod
    def get_pins(pins_count):
        pins = []
        degree = -math.radians(360 / pins_count)

        for i in range(pins_count):
            pin = [
                min(999, 500 - (round(math.sin(degree * i) * 500))),
                min(999, 500 - (round(math.cos(degree * i) * 500)))
            ]
            pins.append(pin)

        # img = Image.open(f"result/original_{sample_name}.png").convert("RGB")
        # img_matrix = np.asarray(img)

        # for i in pins:
        #     img_matrix[min(i[0], 999)][min(i[1], 999)] = [255, 0, 0]

        # tst = Image.fromarray(img_matrix)

        # tst.save(f"result/tmp_{sample_name}.png")
        return pins

    @staticmethod
    def create_board(pins):
        mask = Image.new('RGBA', (1000, 1000), (0, 0, 0, 0))
        draw = ImageDraw.Draw(mask)
        draw.pieslice(((0, 0), (1000, 1000)),
                      0,
                      360,
                      fill=(255, 255, 255),
                      outline="white")

        mask_matrix = np.asarray(mask)
        # print(mask_matrix[0][0])
        for i in pins:
            mask_matrix[i[0]][i[1]] = [255, 0, 0, 1]

        tmp = Image.fromarray(mask_matrix)

        tmp.save("result/board.png")

        return tmp

    @staticmethod
    def draw_line(draw, pin1, pin2):
        draw.line((pin1[0], pin1[1], pin2[0], pin2[1]), fill=0)
