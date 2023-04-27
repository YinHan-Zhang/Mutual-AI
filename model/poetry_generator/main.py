# -*- coding = utf-8 -*-
# @Time: 2023/04/27
# @Software: PyCharm
import tensorflow as tf
from model.poetry_generator.dataset import tokenizer
import model.poetry_generator.settings as settings
import model.poetry_generator.utils as utils


class User:
    """
    # 随机生成一首诗
    # print(utils.generate_random_poetry(tokenizer, model))
    # # 给出部分信息的情况下，随机生成剩余部分
    # print(utils.generate_random_poetry(tokenizer, model, s='床前明月光，'))
    # # 生成藏头诗
    # print(utils.generate_acrostic(tokenizer, model, head='海阔天空'))
    """

    def __init__(self, model):
        self.model = model
        self.token = tokenizer

    def CreatePoem(self):
        return utils.generate_random_poetry(self.token, self.model)

    def CreateNext(self, input='床前明月光，'):
        return utils.generate_random_poetry(self.token, self.model, input)

    def SideHead(self, head='海阔天空'):
        return utils.generate_acrostic(self.token, self.model, head)


# 加载训练好的模型
model = tf.keras.models.load_model(settings.BEST_MODEL_PATH)

user = User(model)


def auto_generate():
    return user.CreatePoem()


def from_first_sentence(first_sentence):
    return user.CreateNext(first_sentence)


def side_head(head):
    return user.SideHead(head)
