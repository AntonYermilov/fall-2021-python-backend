import numpy as np
from typing import List

from .common import Share


def price_weighing(stocks: List[Share]) -> np.ndarray:
    assert all(share.current_price > 0 for share in stocks)

    weights = np.array([stock.current_price for stock in stocks], dtype=np.float32)
    weights /= weights.sum()
    return weights


def inv_price_weighing(stocks: List[Share]) -> np.ndarray:
    assert all(share.current_price > 0 for share in stocks)

    weights = np.array([1.0 / stock.current_price for stock in stocks], dtype=np.float32)
    weights /= weights.sum()
    return weights
