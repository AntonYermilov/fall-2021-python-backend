import unittest

from app.routers.sample_index import SampleIndexRequest, SampleIndexStrategy, StockMarketIndex
from app.routers.sample_index import sample_index


class TestSampleIndex(unittest.TestCase):

    def test_sample_sp100_index_weighed(self):
        request = SampleIndexRequest(
            budget=10000,
            index=StockMarketIndex.sp100,
            strategy=SampleIndexStrategy.index_weighed
        )
        response = sample_index(request)

        self.assertGreaterEqual(len(response.stocks), 1)

        min_price = min(share.current_price for share in response.stocks)
        total_price = sum(share.current_price for share in response.stocks)

        self.assertGreater(total_price + min_price, 10000)
        self.assertLessEqual(min_price, 100)
        self.assertLessEqual(abs(total_price - response.total_price), 1e-4)

    def test_sample_sp500_index_weighed(self):
        request = SampleIndexRequest(
            budget=10000,
            index=StockMarketIndex.sp500,
            strategy=SampleIndexStrategy.index_weighed
        )
        response = sample_index(request)

        self.assertGreaterEqual(len(response.stocks), 1)

        min_price = min(share.current_price for share in response.stocks)
        total_price = sum(share.current_price for share in response.stocks)

        self.assertGreater(total_price + min_price, 10000)
        self.assertLessEqual(min_price, 100)
        self.assertLessEqual(abs(total_price - response.total_price), 1e-4)

    def test_sample_nasdaq100_price_weighed(self):
        request = SampleIndexRequest(
            budget=10000,
            index=StockMarketIndex.nasdaq100,
            strategy=SampleIndexStrategy.price_weighed
        )
        response = sample_index(request)

        self.assertGreaterEqual(len(response.stocks), 1)

        min_price = min(share.current_price for share in response.stocks)
        total_price = sum(share.current_price for share in response.stocks)

        self.assertGreater(total_price + min_price, 10000)
        self.assertLessEqual(min_price, 100)
        self.assertLessEqual(abs(total_price - response.total_price), 1e-4)

    def test_sample_dowjones_inv_price_weighed(self):
        request = SampleIndexRequest(
            budget=10000,
            index=StockMarketIndex.sp100,
            strategy=SampleIndexStrategy.inv_price_weighed
        )
        response = sample_index(request)

        self.assertGreaterEqual(len(response.stocks), 1)

        min_price = min(share.current_price for share in response.stocks)
        total_price = sum(share.current_price for share in response.stocks)

        self.assertGreater(total_price + min_price, 10000)
        self.assertLessEqual(min_price, 100)
        self.assertLessEqual(abs(total_price - response.total_price), 1e-4)

