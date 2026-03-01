from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.clients import http_client # 공유 클라이언트 임포트
from routers import external, game  # 작성한 라우터들 임포트

# 생명주기 관리
@asynccontextmanager
async def lifespan(app: FastAPI):
    http_client.client = httpx.AsyncClient() # HTTP 클라이언트 초기화
    yield
    await http_client.client.aclose() # HTTP 클라이언트 종료

# FastAPI 앱 객체 생성
app = FastAPI(title="Mini Guess Game API", lifespan=lifespan)

# CORS 설정(교차 출처 허용 설정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # 3000번 포트(Next.js) 요청 허용
    allow_credentials=True,                  # 자격 증명 허용
    allow_methods=["*"],                     # 모든 HTTP 메서드 허용
    allow_headers=["*"],                     # 모든 헤더 허용
)

# 라우터 등록 (파일별로 분리한 기능을 연결)
app.include_router(external.router)
app.include_router(game.router)


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}


@app.get("/api/test")
async def test_connection():
    return {"status": "success", "message": "FastAPI와 연결되었습니다!"}

