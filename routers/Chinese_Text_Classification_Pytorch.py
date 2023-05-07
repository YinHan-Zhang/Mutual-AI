from fastapi import APIRouter

from model.Chinese_Text_Classification_Pytorch.test import Predict
from fastapi.responses import JSONResponse

router = APIRouter()


# 文本分类
@router.get("/Chinese_Text_Classification")
async def text_classification(text: str):
    model = Predict()
    res = model.predict(text)

    return JSONResponse({
        "res": res
    })