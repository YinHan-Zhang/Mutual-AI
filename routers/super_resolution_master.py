# -*- coding = utf-8 -*-
# @Time: 2023/05/07
# @Author:XiLinky
# @Software: PyCharm
import model.super_resolution_master.example_edsr
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter()


class Item(BaseModel):
    img: str


@router.post("/super-resolution-master")
async def super_resolution_master(item: Item):
    sr = model.super_resolution_master.example_edsr.resolve_and_plot(item.img)
    return JSONResponse({
        "img": sr
    })
    # return sr

