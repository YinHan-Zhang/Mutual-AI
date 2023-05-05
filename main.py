import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers import liner, written_digit_recognition, poetry_generator

app = FastAPI()

app.docs_url = None
app.redoc_url = None

# 跨域
origins = [
    "http://ai.9998k.cn",
    '127.0.0.1',
    'null'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(liner.router)
app.include_router(written_digit_recognition.router)
app.include_router(poetry_generator.router)


@app.get("/")
async def main():
    return JSONResponse({
        "code": 200
    })


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)
