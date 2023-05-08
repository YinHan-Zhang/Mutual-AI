import argparse

from PIL import Image
import cv2
from starlette.responses import StreamingResponse

from preprocess_image import preprocess_image
import tensorflow as tf
import neuralgym as ng
import base64
import re
from io import BytesIO


from inpaint_model import InpaintCAModel

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
    img = Image.open(image_data)
    if image_path:
        img.save(image_path)
    return img

def watermark_removel(input_Image):
    FLAGS = ng.Config('inpaint.yml')
    # ng.get_gpus(1)
    args, unknown = parser.parse_known_args()
    args.image = base64_to_image(input_Image)
    model = InpaintCAModel()
    image = Image.open(args.image)
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
                    args.checkpoint_dir, from_name)
                assign_ops.append(tf.assign(var, var_value))
            sess.run(assign_ops)
            print('Model loaded.')
            # 别问 问就是拿GPT写的
            result = sess.run(output)
            return result
            # return cv2.imwrite(args.output, cv2.cvtColor(
            #     result[0][:, :, ::-1], cv2.COLOR_BGR2RGB))


