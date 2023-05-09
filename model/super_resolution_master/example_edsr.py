#!/usr/bin/env python
# coding: utf-8
import base64
import os
import re
from io import BytesIO

import tensorflow as tf

import numpy as np
from PIL import Image

# from data import DIV2K
from model.super_resolution_master.model_.edsr import edsr
# from train import EdsrTrainer
from model.super_resolution_master.model_.common import resolve_single
from model.super_resolution_master.utils import load_image, plot_sample

depth = 16
scale = 4

weights_file = os.path.join(os.path.dirname(__file__), 'weights', 'weights.h5')


def base64_to_image(base64_str, image_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    img = img.convert('RGB')
    if image_path:
        img.save(image_path)
    return img


# PIL图片保存为base64编码
def pil_base64(img, coding='utf-8'):
    img_format = img.format
    if img_format == None:
        img_format = 'JPEG'

    format_str = 'JPEG'
    if 'png' == img_format.lower():
        format_str = 'PNG'
    if 'gif' == img_format.lower():
        format_str = 'gif'

    if img.mode == "P":
        img = img.convert('RGB')
    if img.mode == "RGBA":
        format_str = 'PNG'
        img_format = 'PNG'

    output_buffer = BytesIO()
    # img.save(output_buffer, format=format_str)
    img.save(output_buffer, quality=100, format=format_str)
    byte_data = output_buffer.getvalue()
    base64_str = 'data:image/' + img_format.lower() + ';base64,' + base64.b64encode(byte_data).decode(coding)

    return base64_str

def evavalue():
    model = edsr(scale=scale, num_res_blocks=depth)
    model.load_weights(weights_file)

    return model


def resolve_and_plot(lr_image):
    lr_image = base64_to_image(lr_image)
    lr = np.array(lr_image)
    sr = resolve_single(evavalue(), lr)
    # plot_sample(lr, sr)

    encode_image = tf.image.encode_png(sr)
    res = str(base64.b64encode(encode_image.numpy()), 'utf-8')

    return 'data:image/png;base64,' + res
