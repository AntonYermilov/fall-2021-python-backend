from enum import Enum
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.lib.common import Share
from app.lib.market_index import fetch_sp100, fetch_sp500, fetch_dowjones, fetch_nasdaq100
from app.lib.weighing import price_weighing, inv_price_weighing
from app.lib.sampling import sample


router = APIRouter(
    prefix='/sample_index'
)


class StockMarketIndex(str, Enum):
    sp100 = 'sp100'
    sp500 = 'sp500'
    nasdaq100 = 'nasdaq100'
    dowjones = 'dowjones'


class SampleIndexStrategy(str, Enum):
    index_weighed = 'index-weighed'
    price_weighed = 'price-weighed'
    inv_price_weighed = 'inv-price-weighed'


class SampleIndexRequest(BaseModel):
    budget: float
    index: StockMarketIndex
    strategy: SampleIndexStrategy


class SampleIndexResponse(BaseModel):
    stocks: List[Share]
    total_price: float


@router.post('')
async def sample_index(body: SampleIndexRequest):
    if body.budget < 0:
        raise HTTPException(
            status_code=400, detail='Budget can not be negative'
        )

    stocks, index_weights = {
        StockMarketIndex.sp100: fetch_sp100,
        StockMarketIndex.sp500: fetch_sp500,
        StockMarketIndex.nasdaq100: fetch_nasdaq100,
        StockMarketIndex.dowjones: fetch_dowjones
    }[body.index]()

    weights = {
        SampleIndexStrategy.index_weighed: (lambda _: index_weights),
        SampleIndexStrategy.price_weighed: price_weighing,
        SampleIndexStrategy.inv_price_weighed: inv_price_weighing
    }[body.strategy](stocks)

    samples = sample(stocks, weights, body.budget)

    response = SampleIndexResponse(
        stocks=samples,
        total_price=sum(share.current_price for share in samples)
    )

    return response
