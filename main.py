from fastapi import FastAPI

app = FastAPI()
from fastapi.responses import JSONResponse

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

@app.get("/test")
def test():
    return {"message": "Hello FastAPI! test"}

# guess number up, down game
SECRET = 42
@app.get("/guess")
def guess_number(num: int):
    if num < SECRET:
        return {"result": "UP!"}
    elif num > SECRET:
        return {"result": "DOWN!"}
    return JSONResponse(content={"result": "정답!"}, media_type="application/json; charset=utf-8") # 한글 깨짐 방지 처리

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

