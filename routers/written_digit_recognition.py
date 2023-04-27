# -*- coding = utf-8 -*-
# @Time: 2023/04/27
# @Author:MoyiTech
# @Software: PyCharm
from fastapi import APIRouter, FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
import model.written_digit_recognition.main

router = APIRouter()


@router.post("/written_digit_recognition")
async def written_digit_recognition(file: UploadFile):
    print(file.content_type)
    res, used_time = model.written_digit_recognition.main.recognize(file.file)
    return {
        "filename": file.filename,
        "res": res,
        'consume': int(used_time * 1000)
    }

