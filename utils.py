import math

import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFilter


class Utils:
    @staticmethod
    def _gaussian_blur(img):
        return img.filter(ImageFilter.GaussianBlur(radius=10))

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
        rgb_img.save(f"result/r_{sample_name}.png")

        blured = Utils._gaussian_blur(rgb_img)
        blured.save(f"result/r_b_{sample_name}.png")

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

        for i in pins:
            mask_matrix[i[0]][i[1]] = [255, 0, 0, 1]

        tmp = Image.fromarray(mask_matrix)

        tmp.save("result/board.png")

        return tmp

    @staticmethod
    def draw_line(draw, pin1, pin2):
        draw.line((pin1[0], pin1[1], pin2[0], pin2[1]), fill=0)

    @staticmethod
    def save_board(board):
        board.save("result/board.png")

    @staticmethod
    def get_blured_new_board(board, pins_order):
        draw = ImageDraw.Draw(board)
        for i in range(len(pins_order) - 1):
            Utils.draw_line(draw, pins_order[i], pins_order[i + 1])

        blured_board = Utils._gaussian_blur(board)
        blured_board_array = np.array(blured_board)
        return blured_board_array
