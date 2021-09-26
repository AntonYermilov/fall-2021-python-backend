import unittest

import numpy as np

from app.lib.common import Share
from app.lib.weighing import price_weighing, inv_price_weighing


class TestPriceWeighing(unittest.TestCase):
    def test_same_price(self):
        stocks = [
            Share(ticker='a', current_price=1),
            Share(ticker='b', current_price=1),
            Share(ticker='c', current_price=1),
            Share(ticker='d', current_price=1)
        ]

        weights = price_weighing(stocks)
        expected_weights = np.full(4, 0.25)

        diff = np.abs(weights - expected_weights)
        self.assertTrue(np.all(diff < 1e-5))

    def test_different_price(self):
        stocks = [
            Share(ticker='a', current_price=1),
            Share(ticker='b', current_price=2),
            Share(ticker='c', current_price=3),
            Share(ticker='d', current_price=4)
        ]

        weights = price_weighing(stocks)
        expected_weights = np.array([0.1, 0.2, 0.3, 0.4])

        diff = np.abs(weights - expected_weights)
        self.assertTrue(np.all(diff < 1e-5))

    def test_weights_sum(self):
        stocks = [
            Share(ticker='a', current_price=1),
            Share(ticker='b', current_price=2),
            Share(ticker='c', current_price=3),
            Share(ticker='d', current_price=4)
        ]

        weights = price_weighing(stocks)
        error = np.abs(weights.sum() - 1.0)

        self.assertTrue(error < 1e-5)


class TestInvPriceWeighing(unittest.TestCase):
    def test_same_price(self):
        stocks = [
            Share(ticker='a', current_price=1),
            Share(ticker='b', current_price=1),
            Share(ticker='c', current_price=1),
            Share(ticker='d', current_price=1)
        ]

        weights = inv_price_weighing(stocks)
        expected_weights = np.full(4, 0.25)

        diff = np.abs(weights - expected_weights)
        self.assertTrue(np.all(diff < 1e-5))

    def test_different_price(self):
        stocks = [
            Share(ticker='a', current_price=1),
            Share(ticker='b', current_price=4),
            Share(ticker='c', current_price=2),
            Share(ticker='d', current_price=4)
        ]

        weights = inv_price_weighing(stocks)
        expected_weights = np.array([0.5, 0.125, 0.25, 0.125])

        diff = np.abs(weights - expected_weights)
        self.assertTrue(np.all(diff < 1e-5))

    def test_weights_sum(self):
        stocks = [
            Share(ticker='a', current_price=1),
            Share(ticker='b', current_price=2),
            Share(ticker='c', current_price=3),
            Share(ticker='d', current_price=4)
        ]

        weights = inv_price_weighing(stocks)
        error = np.abs(weights.sum() - 1.0)

        self.assertTrue(error < 1e-5)
