from fastapi import APIRouter

router = APIRouter(prefix="/system", tags=[""])

@router.get("/health")
async def test_connection():
    return {"status": "success", "message": "FastAPI와 연결되었습니다!"}

