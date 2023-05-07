# -*- coding = utf-8 -*-
# @Time: 2023/05/07
# @Author:XiLinky
# @Software: PyCharm
from routers.super_resolution_master import resolve_and_plot
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter()


class Item(BaseModel):
    img: str


@router.post("/super-resolution-master")
async def super_resolution_master(item: Item):
    sr = resolve_and_plot(item.img)
    return JSONResponse({
        "img": sr
    })
    # return sr

