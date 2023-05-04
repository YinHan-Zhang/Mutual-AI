from fastapi import APIRouter
from fastapi.responses import JSONResponse
from model import Liner

router = APIRouter()
liner_model = Liner.Liner_Model()


@router.get("/liner")
async def liner(data: int):
    data: int
    return JSONResponse({
        "code": 200,
        "data": {
            "result": liner_model.run(data)
        }
    })