from io import BytesIO

from fastapi import APIRouter
from starlette.responses import StreamingResponse

import model.watermark_removal.main

# 由于tensorflow 使用的1.14版本 与main函数其他模型不兼容先不导进来
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import cv2

router = APIRouter()


class Item(BaseModel):
    img: str


@router.post("/watermark_removal")
async def watermark_removal(item: Item):
    print(1)
    result = model.watermark_removal.main.watermark_removel(item.img)
    # img = cv2.imdecode(result, cv2.IMREAD_COLOR)
    # result_2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_bytes = cv2.imencode('.jpg', result_2)[1].tobytes()
    return {
        'res': result
    }