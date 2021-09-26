from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_negative_budget():
    response = client.post(
        url='/sample_index',
        headers={'Content-Type': 'application/json'},
        json={'budget': -10000, 'index': 'sp100', 'strategy': 'index-weighed'}
    )

    assert response.status_code == 400


def test_sample_sp100_index_weighed():
    response = client.post(
        url='/sample_index',
        headers={'Content-Type': 'application/json'},
        json={'budget': 10000, 'index': 'sp100', 'strategy': 'index-weighed'}
    )

    assert response.status_code == 200
    assert 9900 <= response.json()['total_price'] <= 10000


def test_sample_sp500_index_weighed():
    response = client.post(
        url='/sample_index',
        headers={'Content-Type': 'application/json'},
        json={'budget': 10000, 'index': 'sp100', 'strategy': 'index-weighed'}
    )

    assert response.status_code == 200
    assert 9900 <= response.json()['total_price'] <= 10000


def test_sample_nasdaq100_price_weighed():
    response = client.post(
        url='/sample_index',
        headers={'Content-Type': 'application/json'},
        json={'budget': 10000, 'index': 'nasdaq100', 'strategy': 'price-weighed'}
    )

    assert response.status_code == 200
    assert 9900 <= response.json()['total_price'] <= 10000


def test_sample_dowjones_inv_price_weighed():
    response = client.post(
        url='/sample_index',
        headers={'Content-Type': 'application/json'},
        json={'budget': 10000, 'index': 'dowjones', 'strategy': 'inv-price-weighed'}
    )

    assert response.status_code == 200
    assert 9900 <= response.json()['total_price'] <= 10000
