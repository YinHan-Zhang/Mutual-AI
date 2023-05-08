from fastapi import APIRouter
import model.watermark_removal.main

# 由于tensorflow 使用的1.14版本 与main函数其他模型不兼容先不导进来
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import cv2
from starlette.responses import StreamingResponse
from io import BytesIO
import base64
router = APIRouter()


class Item(BaseModel):
    img: str


# @router.post("/watermark_removal")
# async def watermark_removal(item: Item):
#     result = model.watermark_removal.main.recognize(item.img)
#     img = cv2.imdecode(result, cv2.IMREAD_COLOR)
#     result_2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     img_bytes = cv2.imencode('.jpg', result_2)[1].tobytes()
#     return StreamingResponse(BytesIO(img_bytes), media_type="image/jpeg")
