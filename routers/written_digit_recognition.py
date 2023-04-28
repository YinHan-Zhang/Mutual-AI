# -*- coding = utf-8 -*-
# @Time: 2023/04/27
# @Author:MoyiTech
# @Software: PyCharm
from fastapi import APIRouter, FastAPI, File, Form, UploadFile
import model.written_digit_recognition.main
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    img: str


@router.post("/written_digit_recognition")
async def written_digit_recognition(item: Item):
    res, used_time = model.written_digit_recognition.main.recognize(item.img)
    return {
        "res": res,
        'consume': int(used_time * 1000)
    }
