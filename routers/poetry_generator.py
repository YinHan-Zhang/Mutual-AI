# -*- coding = utf-8 -*-
# @Time: 2023/04/27
# @Software: PyCharm
from fastapi import APIRouter

from model.poetry_generator.main import auto_generate, from_first_sentence, side_head
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/poetry-generator")
async def poetry_generator(type_choice: int, addition=''):
    if type_choice == 1:
        res = auto_generate()
    elif type_choice == 2:
        res = from_first_sentence(addition)
    elif type_choice == 3:
        res = side_head(addition)

    return JSONResponse({
        "res": res
    })