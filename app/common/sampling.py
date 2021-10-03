import numpy as np
from typing import List

from .common import Share


def sample(stocks: List[Share], weights: np.ndarray, budget: float) -> List[Share]:
    assert len(stocks) == len(weights)
    assert np.all(weights >= 0)

    result = []

    indices = np.arange(len(stocks))
    stock_price = np.array([stock.current_price for stock in stocks], dtype=np.float32)

    mask = stock_price <= budget
    while np.any(mask):
        w = weights * mask
        p = w / w.sum()
        i = np.random.choice(indices, p=p)
        result.append(stocks[i])
        budget -= stocks[i].current_price
        mask = stock_price <= budget

    return result
