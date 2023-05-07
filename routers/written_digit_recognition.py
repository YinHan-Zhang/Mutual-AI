# -*- coding = utf-8 -*-
# @Time: 2023/04/27
# @Author:MoyiTech
# @Software: PyCharm
from fastapi import APIRouter
import model.written_digit_recognition.main
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter()


class Item(BaseModel):
    img: str


# 接收base64编码后的二进制流处理后返回数据
@router.post("/written_digit_recognition")
async def written_digit_recognition(item: Item):
    res, used_time = model.written_digit_recognition.main.recognize(item.img)
    return JSONResponse({
        "res": res,
        'consume': int(used_time * 1000)
    })