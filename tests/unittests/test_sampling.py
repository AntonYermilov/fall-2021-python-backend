import unittest

import numpy as np
from collections import defaultdict

from app.lib.common import Share
from app.lib.sampling import sample


class TestSampling(unittest.TestCase):
    def test_number_of_samples_equal_price(self):
        stocks = [
            Share(ticker='a', current_price=1),
            Share(ticker='b', current_price=1),
            Share(ticker='c', current_price=1),
            Share(ticker='d', current_price=1)
        ]
        weights = np.ones(4)

        for i in range(100):
            samples = sample(stocks, weights, i + 1)
            self.assertEqual(len(samples), i + 1)

    def test_number_of_samples_different_price(self):
        stocks = [
            Share(ticker='a', current_price=1),
            Share(ticker='b', current_price=2),
            Share(ticker='c', current_price=3),
            Share(ticker='d', current_price=4)
        ]
        weights = np.ones(4)

        for i in range(100):
            samples = sample(stocks, weights, 24)
            self.assertGreaterEqual(len(samples), 6)
            self.assertLessEqual(len(samples), 24)

    def test_zero_weights(self):
        stocks = [
            Share(ticker='a', current_price=1),
            Share(ticker='b', current_price=1),
            Share(ticker='c', current_price=1),
            Share(ticker='d', current_price=1)
        ]

        for i in range(4):
            weights = np.zeros(4)
            weights[i] = 1
            samples = sample(stocks, weights, 100)
            self.assertTrue(all(share.ticker == stocks[i].ticker for share in samples))

    def test_different_weights(self):
        stocks = [
            Share(ticker='a', current_price=1),
            Share(ticker='b', current_price=1),
            Share(ticker='c', current_price=1),
            Share(ticker='d', current_price=1)
        ]
        weights = np.arange(1, 5)

        samples = sample(stocks, weights, 1000)
        counts = defaultdict(int)
        for share in samples:
            counts[share.ticker] += 1

        for i in range(3):
            self.assertLessEqual(counts[stocks[i].ticker], counts[stocks[i + 1].ticker])
