import requests
import pandas as pd
import numpy as np
from typing import List, Tuple

from .common import Share


def _fetch_index(index: str) -> Tuple[List[Share], np.ndarray]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
        'X-Requested-With': 'XMLHttpRequest'
    }
    resp = requests.get(f'https://www.slickcharts.com/{index}', headers=headers)

    df = pd.read_html(resp.text)[0]
    stocks = [Share(ticker=row['Symbol'], current_price=row['Price']) for _, row in df.iterrows()]
    weights = np.array([row['Weight'] / row['Price'] for _, row in df.iterrows()])
    return stocks, weights


def fetch_sp100() -> Tuple[List[Share], np.ndarray]:
    stocks, weights = _fetch_index('sp500')
    return stocks[:100], weights[:100]


def fetch_sp500() -> Tuple[List[Share], np.ndarray]:
    stocks, weights = _fetch_index('sp500')
    return stocks[:500], weights[:500]


def fetch_nasdaq100() -> Tuple[List[Share], np.ndarray]:
    stocks, weights = _fetch_index('nasdaq100')
    return stocks[:100], weights[:100]


def fetch_dowjones() -> Tuple[List[Share], np.ndarray]:
    return _fetch_index('dowjones')
