import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import liner, written_digit_recognition, poetry_generator

app = FastAPI()

app.docs_url = None
app.redoc_url = None


origins = [
    "api.9998k.cn",
    "127.0.0.1",
    "null"
]

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if request.method != "OPTIONS":
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = origins
        return response


app.include_router(liner.router)
app.include_router(written_digit_recognition.router)
app.include_router(poetry_generator.router)

@app.get("/")
async def main():
    return JSONResponse({
        "code": 200
    })


@app.options("/{path:path}")
async def preflight():
    headers = {
        "Access-Control-Allow-Origin": origins,
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "*"
    }
    return JSONResponse({
        "code": 200
    }, headers=headers)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)
