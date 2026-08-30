from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yfinance as yf
from datetime import datetime, timedelta

# Stock API
router = APIRouter(prefix="/stock", tags=["stock"])

class ReturnRequest(BaseModel):
    ticker: str
    buy_date: str   # YYYY-MM-DD
    buy_amount: float
    sell_date: str  # YYYY-MM-DD

# 1. 주식 검색 API
@router.get("/search")
def search_stock(keyword: str):
    try:
        ticker = yf.Ticker(keyword)
        info = ticker.info
        # 최소한의 정보가 있는지 확인
        if not info or 'symbol' not in info:
            raise HTTPException(status_code=404, detail="주식을 찾을 수 없습니다.")

        return {
            "ticker": keyword.upper(),
            "name": info.get("longName", keyword.upper()),
            "currency": info.get("currency", "USD")
        }
    except Exception:
        raise HTTPException(status_code=404, detail="정확한 티커를 입력하세요. (예: AAPL, 005930.KS)")

# 2. 수익률 계산 API
@router.post("/calculate")
def calculate_return(req: ReturnRequest):
    try:
        ticker = yf.Ticker(req.ticker)

        # 주말/공휴일을 고려하여 검색 날짜 범위를 조금 넓게 설정
        start_dt = req.buy_date
        end_dt = (datetime.strptime(req.sell_date, "%Y-%m-%d") + timedelta(days=5)).strftime("%Y-%m-%d")

        df = ticker.history(start=start_dt, end=end_dt)

        if df.empty:
            raise HTTPException(status_code=400, detail="해당 기간의 주가 데이터가 존재하지 않습니다.")

        # 입력일 기준 가장 가까운 첫 영업일(매수), 마지막 영업일(매도) 추출
        buy_df = df.loc[df.index >= req.buy_date]
        sell_df = df.loc[df.index <= req.sell_date]

        if buy_df.empty or sell_df.empty:
            raise HTTPException(status_code=400, detail="선택한 날짜 범위에 유효한 영업일 데이터가 없습니다.")

        buy_price = buy_df.iloc[0]['Close']
        sell_price = sell_df.iloc[-1]['Close']

        # 계산 공식 적용
        shares_owned = req.buy_amount / buy_price
        sell_amount = shares_owned * sell_price
        profit = sell_amount - req.buy_amount
        return_rate = (profit / req.buy_amount) * 100

        return {
            "buy_price": round(buy_price, 2),
            "sell_price": round(sell_price, 2),
            "shares_owned": round(shares_owned, 4),
            "sell_amount": round(sell_amount, 2),
            "profit": round(profit, 2),
            "return_rate": round(return_rate, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


