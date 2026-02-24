from fastapi import FastAPI, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import random
import httpx


# 공유할 클라이언트를 담을 클래스 혹은 변수
class HttpClient:
    client: httpx.AsyncClient = None

http_client = HttpClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # [App 시작] 클라이언트 생성 (커넥션 풀 시작)
    http_client.client = httpx.AsyncClient(base_url="https://api.example.com")
    yield
    await http_client.client.aclose() # [App 종료] 클라이언트 닫기

app = FastAPI(title="Mini Guess Game API", lifespan=lifespan)

# CORS 설정: Next.js(3000번 포트)로부터의 요청을 허용합니다
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Next.js 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/test")
async def test_connection():
    return {
        "status": "success", 
        "message": "FastAPI와 연결되었습니다!"
	}


# JsonPlaceHolder API
@app.get("/api/posts")
async def getPosts():
    url = "https://jsonplaceholder.typicode.com/posts"

    response = await http_client.client.get(url)
    response = response.json()

    return response


@app.get("/api/comments")
async def getPosts():
    url = "https://jsonplaceholder.typicode.com/comments"

    response = await http_client.client.get(url)
    response = response.json()

    return response


@app.get("/api/users")
async def getUsers():
    url = "https://jsonplaceholder.typicode.com/users"

    response = await http_client.client.get(url)
    response = response.json()

    return response











@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

@app.get("/test")
def test():
    return {"message": "Hello FastAPI! test"}

# guess number up, down game
# SECRET = 42
# @app.get("/guess")
# def guess_number(num: int):
#     if num < SECRET:
#         return {"result": "UP!"}
#     elif num > SECRET:
#         return {"result": "DOWN!"}
#     return JSONResponse(content={"result": "정답!"}, media_type="application/json; charset=utf-8") # 한글 깨짐 방지 처리

# guess random number up&down game upgrade
SECRET = 0 # 전역변수 초기화
# 요청 Body 스키마(Body 검증)
class GuessRequest(BaseModel):
    number: int

# 의존성 (게임 상태 제공)
def get_secret_number():
	global SECRET
	if SECRET == 0: # 0일 경우 secret(정답)
		random_number = random.randint(1, 100) # 랜덤 값(정답) 초기화
		SECRET = random_number # 전역 변수에 저장
	else: # secret(정답) 값이 있을 경우 값 유지
		random_number = SECRET
	return random_number

# API
@app.post("/guess")
def guess_number(
    guess: GuessRequest, # Body 자동 검증
    secret: int = Depends(get_secret_number), # 의존성 주입
    user: str = Query(..., description="플레이어 이름") # 쿼리 파라미터 사용
):
	global SECRET
	if guess.number < secret:
		result = "UP"
	elif guess.number > secret:
		result = "DOWN"
	else:
		result = "정답 🎉"
		SECRET = 0

	return {
		"user": user,
		"guess": guess.number,
		"result": result,
		"answer": secret
    }

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


