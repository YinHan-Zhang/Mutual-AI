"""Reload and serve a saved model"""
import json
import jieba
from pathlib import Path
from tensorflow.contrib import predictor
from functools import partial

PARAMS = './chinese_sentiment/results/params.json'



def predict(pred_fn, line, length=300):
    sentence = ' '.join(jieba.cut(line.strip(), cut_all=False, HMM=True))
    words = [w.encode() for w in sentence.strip().split()]
    if len(words) >= length:
        words = words[:length]
    else:
        words.extend(['<pad>'] * (length - len(words)))
    predictions = pred_fn({'words': [words]})
    return predictions



def run(inp):
    with Path(PARAMS).open() as f:
        params = json.load(f)
    export_dir = './chinese_sentiment/saved_model'
    subdirs = [x for x in Path(export_dir).iterdir()
               if x.is_dir() and 'temp' not in str(x)]
    latest = str(sorted(subdirs)[-1])
    predict_fn = partial(predict, predictor.from_saved_model(latest))
    line = inp
    res = predict_fn(line, params['nwords'])
    return str(res['labels'])