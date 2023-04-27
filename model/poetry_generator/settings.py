# -*- coding = utf-8 -*-
# @Time: 2023/04/27
# @Software: PyCharm
# 禁用词，包含如下字符的唐诗将被忽略
import os
DISALLOWED_WORDS = ['（', '）', '(', ')', '__', '《', '》', '【', '】', '[', ']']
# 句子最大长度
MAX_LEN = 64
# 最小词频
MIN_WORD_FREQUENCY = 8
# 训练的batch size
BATCH_SIZE = 16
# 数据集路径
DATASET_PATH = os.path.join(os.path.dirname(__file__), './poetry.txt')
# 每个epoch训练完成后，随机生成SHOW_NUM首古诗作为展示
SHOW_NUM = 5
# 共训练多少个epoch
TRAIN_EPOCHS = 1
# 最佳权重保存路径
BEST_MODEL_PATH = os.path.join(os.path.dirname(__file__), './test_model.h5')
