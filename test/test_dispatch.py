from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_dispatch():
    data = [
        {
            "id": "1",
            "orderId": "1",
            "sku": "la-tournee-cafe-grains-espresso-370",
            "unitCount": 1,
        },
        {
            "id": "2",
            "orderId": "1",
            "sku": "pajo-lait-amande-avoine-bio-75",
            "unitCount": 1,
        },
        {"id": "3", "orderId": "1", "sku": "orangina-25", "unitCount": 6},
        {
            "id": "4",
            "orderId": "1",
            "sku": "coca-cola-cherry-33",
            "unitCount": 12,
        },
    ]
    response = client.post("/api/v1/orders/dispatch", json=data)
    data = response.json()
    assert data == {"Supplier": 0, "Slot6": 1, "Slot12": 0, "Slot20": 1}
