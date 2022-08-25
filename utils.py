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

        img_cropped.save(f"result/r_{sample_name}.png")

        size = (w, h)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice(((0, 0), (h, w)), 0, 360, fill=255, outline="white")

        img_arr = np.array(img_cropped, dtype='uint8')
        mask_arr = np.array(mask)
        final_img_arr = np.dstack((img_arr, mask_arr))

        result = Image.fromarray(final_img_arr)
        result.resize((1000, 1000)).save(f"result/r_{sample_name}.png")

        rgb_img = Image.open(f"result/r_{sample_name}.png").convert('L')
        rgb_img.save(f"result/r_{sample_name}.png")
