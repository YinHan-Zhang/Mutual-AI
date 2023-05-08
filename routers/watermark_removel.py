from fastapi import APIRouter
# import model.watermark_removal.main

# 由于tensorflow 使用的1.14版本 与main函数其他模型不兼容先不导进来
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter()


class Item(BaseModel):
    img: str


# @router.post("/")
# async def watermark_removal(item: Item):
#     res = model.watermark_removal.main.recognize(item.img)
#     return JSONResponse({
#         "res": res,
#     })