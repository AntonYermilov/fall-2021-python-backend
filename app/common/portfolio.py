import json
from enum import Enum
from pydantic import BaseModel
from typing import List
from datetime import datetime
import pickle


class ShareEventType(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class ShareEvent(BaseModel):
    type: ShareEventType
    price: float
    count: int
    date: datetime


class Share(BaseModel):
    ticker: str
    current_price: float


class ShareInfo(BaseModel):
    share: Share
    events: List[ShareEvent]

    @property
    def lots(self):
        return sum(e.count for e in self.events if e.type == ShareEventType.BUY) - \
               sum(e.count for e in self.events if e.type == ShareEventType.SELL)


class Portfolio(BaseModel):
    stocks: List[ShareInfo]

    def dump(self, portfolio_path: str):
        with open(portfolio_path, 'w') as fp:
            fp.write(pickle.dumps(self))

    def load(self, portfolio_path: str):
        with open(portfolio_path, 'r') as fp:
            o = pickle.loads(fp.read())
        self.parse_obj(o)


portfolio = Portfolio(stocks=[])
