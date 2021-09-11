import requests
import pandas as pd
import numpy as np
import yfinance as yf
from argparse import ArgumentParser
from flask import Flask
from flask_pydantic import validate
from pydantic import BaseModel
from typing import List, Union
from enum import Enum

app = Flask(__name__)


class StockMarketIndex(str, Enum):
    sp100 = 'sp100'
    sp500 = 'sp500'


class SampleIndexStrategy(str, Enum):
    random = 'random'
    fixed = 'fixed'


class SampleIndexRequest(BaseModel):
    budget: float
    index: StockMarketIndex
    strategy: SampleIndexStrategy


class Position(BaseModel):
    company: str
    ticker: str
    price: float
    lots: int


class SampleIndexResponse(BaseModel):
    positions: List[Position]
    total_price: float


def fetch_sp(n: int) -> pd.DataFrame:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
        'X-Requested-With': 'XMLHttpRequest'
    }
    r = requests.get('https://www.slickcharts.com/sp500', headers=headers)
    r = pd.read_html(r.text)[0][:n]

    index = pd.DataFrame(columns=['Company', 'Ticker', 'Weight'])
    index['Company'] = r['Company']
    index['Ticker'] = r['Symbol'].str.replace('.', '-')
    index['Weight'] = r['Weight'] / r['Weight'].sum()
    return index


def get_today_price(tickers: str, price_type: str = 'Close') -> Union[float, List[float]]:
    info = yf.download(tickers, period='1d', progress=False, prepost=True, interval='1h')
    today_row = info.fillna(method='ffill').iloc[-1, :]
    tickers = tickers.split()
    price = today_row[price_type]
    if len(tickers) == 1:
        return float(price)
    return [float(price[ticker]) for ticker in tickers]


@app.route('/api/sample_sp500', methods=['POST'])
@validate()
def sample_index(body: SampleIndexRequest):
    if body.budget < 0:
        return {'error': 'Budget can not be negative'}, 400

    try:
        samples = None
        if body.index == StockMarketIndex.sp500:
            samples = fetch_sp(n=500)
        elif body.index == StockMarketIndex.sp100:
            samples = fetch_sp(n=100)
    except:
        return {'error': 'Failed to fetch index weights'}, 500

    try:
        samples['Price'] = get_today_price(' '.join(samples['Ticker'].to_numpy()))
    except:
        return {'error': 'Failed to fetch share prices from Yahoo Finances'}, 500

    if body.strategy == SampleIndexStrategy.fixed:
        # price * lots / budget = weight
        samples['Lots'] = (samples['Weight'] * body.budget / samples['Price']).astype(int)
    else:
        lots = np.zeros(len(samples))
        # TODO: implement
        samples['Lots'] = lots

    positions = [
        Position(
            company=sample['Company'],
            ticker=sample['Ticker'],
            price=sample['Price'],
            lots=sample['Lots']
        ) for _, sample in samples.iterrows() if sample['Lots'] > 0
    ]
    response = SampleIndexResponse(
        positions=positions,
        total_price=sum(map(lambda position: position.price * position.lots, positions))
    )
    return response


class StockPriceResponse(BaseModel):
    ticker: str
    price: float


@app.route('/api/stock_price/<ticker>', methods=['GET'])
@validate()
def stock_price(ticker: str):
    try:
        price = get_today_price(ticker)
    except IndexError:
        return {'error': f'Failed to fetch {ticker} price from Yahoo Finances, probably ticker is delisted'}, 400
    except:
        return {'error': f'Failed to fetch {ticker} price from Yahoo Finances, probably service is down'}, 500
    return StockPriceResponse(ticker=ticker, price=price)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
