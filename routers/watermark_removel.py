from fastapi import APIRouter
# import model.watermark_removal.main
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