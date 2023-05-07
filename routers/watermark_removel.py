from fastapi import APIRouter
import model.watermark_removal.main
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter()


class Item(BaseModel):
    img: str


@router.post("/")
async def written_digit_recognition(item: Item):
    res, used_time = model.watermark_removal.main.recognize(item.img)
    return JSONResponse({
        "res": res,
        'consume': int(used_time * 1000)
    })