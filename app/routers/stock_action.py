import strawberry
from strawberry.asgi import GraphQL
from fastapi import APIRouter
from datetime import datetime
from typing import List

from app.common import portfolio
from app.common.portfolio import portfolio as my_portfolio


@strawberry.type
class ShareEvent:
    type: str
    price: float
    count: int
    date: datetime


@strawberry.type
class Share:
    ticker: str
    avg_buy_price: float
    events: List[ShareEvent]


@strawberry.type
class Query:
    @strawberry.field
    def share(self, ticker: str) -> Share:
        share = Share(ticker=ticker, avg_buy_price=0.0, events=[])
        for stock in my_portfolio.stocks:
            if stock.ticker != ticker:
                continue
            buy_price = []
            for event in stock.events:
                share.events.append(ShareEvent(
                    type=event.type,
                    price=event.price,
                    count=event.count,
                    date=datetime
                ))
                if event.type == portfolio.ShareEventType.BUY:
                    buy_price.extend(event.price for _ in range(event.count))
                else:
                    buy_price = buy_price[event.count:]
                share.avg_buy_price = sum(buy_price) / max(len(buy_price), 1)
        return share


schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)

router = APIRouter(prefix='/TODO')
router.add_route('', graphql_app)
router.add_websocket_route('', graphql_app)
