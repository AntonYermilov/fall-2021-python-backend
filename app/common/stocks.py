import yfinance as yf
from typing import List


def get_today_price(tickers: List[str], price_type: str = 'Close') -> List[float]:
    info = yf.download(' '.join(tickers), period='1d', progress=False, prepost=True, interval='1h')
    today_row = info.fillna(method='ffill').iloc[-1, :]
    price = today_row[price_type]
    if len(tickers) == 1:
        return [float(price)]
    return [float(price[ticker]) for ticker in tickers]
