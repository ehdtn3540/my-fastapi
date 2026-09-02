from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.clients import http_client
import json

# Weather API
router = APIRouter(prefix="/weather", tags=["weather"])


# 날씨 검색 테스트 API
@router.get("/test")
async def test(appid: str):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID={appid}&lang=kr&units=metric"
        response = await http_client.client.get(url)

        import json
        return {
            "response": json.load(response)
        }
    except Exception:
        raise HTTPException(status_code=404, detail="API KEY 또는 요청 URL을 확인해주세요.")

