from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
import random

router = APIRouter(prefix="/guess", tags=["game"])

SECRET = 0

class GuessRequest(BaseModel):
    number: int

def get_secret_number():
    global SECRET
    if SECRET == 0:
        SECRET = random.randint(1, 100)
    return SECRET

@router.post("")
def guess_number(
    guess: GuessRequest,
    secret: int = Depends(get_secret_number),
    user: str = Query(..., description="플레이어 이름")
):
    global SECRET
    if guess.number < secret:
        result = "UP"
    elif guess.number > secret:
        result = "DOWN"
    else:
        result = "정답 🎉"
        SECRET = 0

    return {"user": user, "guess": guess.number, "result": result, "answer": secret}
