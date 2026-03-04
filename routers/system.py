from fastapi import APIRouter

router = APIRouter(prefix="", tags=[""])

@router.get("/api/test")
async def test_connection():
    return {"status": "success", "message": "FastAPI와 연결되었습니다!"}

