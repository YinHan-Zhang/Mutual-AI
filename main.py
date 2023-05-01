import uvicorn
from fastapi import FastAPI
from routers import liner, written_digit_recognition, poetry_generator
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(liner.router)
app.include_router(written_digit_recognition.router)
app.include_router(poetry_generator.router)

app.docs_url = None
app.redoc_url = None

origins = [
    "http://api.9998k.cn",
    "https://api.9998k.cn:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    return JSONResponse({
        "code": 200
    }, headers=headers)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)