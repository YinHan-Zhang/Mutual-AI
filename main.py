import uvicorn
from fastapi import FastAPI
from routers import liner, written_digit_recognition, poetry_generator
from fastapi.responses import JSONResponse

app = FastAPI()

app.include_router(liner.router)
app.include_router(written_digit_recognition.router)
app.include_router(poetry_generator.router)

app.docs_url = None
app.redoc_url = None

# test
# 我就是测试一下
@app.get("/")
async def main():
    return JSONResponse({
        "code": 200
    })

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)