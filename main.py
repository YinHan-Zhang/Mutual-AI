from fastapi import FastAPI
from routers import liner, written_digit_recognition
from fastapi.responses import JSONResponse

app = FastAPI()

app.include_router(liner.router)
app.include_router(written_digit_recognition.router)

app.docs_url = None
app.redoc_url = None


@app.get("/")
async def main():
    return JSONResponse({
        "code": 200
    })
