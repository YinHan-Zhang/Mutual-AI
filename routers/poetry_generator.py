# -*- coding = utf-8 -*-
# @Time: 2023/04/27
# @Software: PyCharm
from fastapi import APIRouter

from model.poetry_generator.main import auto_generate, from_first_sentence, side_head
from fastapi.responses import JSONResponse

router = APIRouter()


# 古诗词生成
@router.get("/poetry-generator")
async def poetry_generator(type_choice: int, addition=''):
    # 自动生成
    if type_choice == 1:
        res = auto_generate()
    # 写第一句诗输出
    elif type_choice == 2:
        res = from_first_sentence(addition)
    # 藏头诗
    elif type_choice == 3:
        res = side_head(addition)

    return JSONResponse({
        "res": res
    })