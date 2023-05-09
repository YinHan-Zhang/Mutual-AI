import argparse
import os.path

from PIL import Image


import sys

import tensorflow as tf
import neuralgym as ng
import base64
import re
from io import BytesIO

sys.path.append('model/watermark_removal')
from inpaint_model import InpaintCAModel
import cv2
from preprocess_image import preprocess_image



parser = argparse.ArgumentParser()
parser.add_argument('--image', default='', type=str,
                    help='The filename of image to be completed.')
parser.add_argument('--output', default='output.png', type=str,
                    help='Where to write output.')
parser.add_argument('--watermark_type', default='istock', type=str,
                    help='The watermark type')
parser.add_argument('--checkpoint_dir', default='model/', type=str,
                    help='The directory of tensorflow checkpoint.')

checkpoint_dir = 'model/'

def base64_to_image(base64_str, image_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    return image_data
    # img = Image.open(image_data)
    # if image_path:
    #     img.save(image_path)
    # return img


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


def watermark_removel(input_Image):
    print(12)
    # FLAGS = ng.Config('inpaint.yml')
    FLAGS = ng.Config(os.path.join(os.path.dirname(__file__), 'inpaint.yml'))
    print(2)
    # ng.get_gpus(1)
    args, unknown = parser.parse_known_args()
    image_input = base64_to_image(input_Image)
    model = InpaintCAModel()
    image = Image.open(image_input).convert('RGB')
    input_image = preprocess_image(image, args.watermark_type)
    tf.reset_default_graph()

    sess_config = tf.ConfigProto()
    sess_config.gpu_options.allow_growth = True
    if (input_image.shape != (0,)):
        with tf.Session(config=sess_config) as sess:
            input_image = tf.constant(input_image, dtype=tf.float32)
            output = model.build_server_graph(FLAGS, input_image)
            output = (output + 1.) * 127.5
            output = tf.reverse(output, [-1])
            output = tf.saturate_cast(output, tf.uint8)
            # load pretrained model
            vars_list = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
            assign_ops = []
            for var in vars_list:
                vname = var.name
                from_name = vname
                var_value = tf.contrib.framework.load_variable(
                    (os.path.join(os.path.dirname(__file__), 'model/')), from_name)
                assign_ops.append(tf.assign(var, var_value))
            sess.run(assign_ops)
            print('Model loaded.')
            # 别问 问就是拿GPT写的
            result = sess.run(output)
            # print(type(result))
            img = Image.fromarray(result[0][:, :, ::-1])
            res = pil_base64(img)
            return res
            # return cv2.imwrite(args.output, cv2.cvtColor(
            #     result[0][:, :, ::-1], cv2.COLOR_BGR2RGB))


