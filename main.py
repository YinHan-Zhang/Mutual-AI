from fastapi import FastAPI
from routers import liner
from model import Liner
from fastapi.responses import JSONResponse

app = FastAPI()



app.include_router(liner.router)


app.docs_url = None
app.redoc_url = None

# test
# 我就是测试一下
@app.get("/")
async def main():
    return JSONResponse({
        "code": 200
    })
