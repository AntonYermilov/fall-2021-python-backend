from fastapi import FastAPI
from app.routers import sample_index, stock_action
from app.common.portfolio import portfolio

portfolio.load('portfolio.pkl')

app = FastAPI()
app.include_router(sample_index.router)
app.include_router(stock_action.router)
