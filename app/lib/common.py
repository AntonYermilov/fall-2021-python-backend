from enum import Enum
from pydantic import BaseModel
from typing import List
from datetime import datetime


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
