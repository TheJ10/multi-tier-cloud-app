from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app import db, crud

client = TestClient(app)

def setup_module():
    # ensure a clean DB for tests: remove DB file if exists and init fresh
    try:
        import os
        os.remove(str(db.DB_PATH))
    except FileNotFoundError:
        pass
    db.init_db()

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_products_and_orders():
    # seed sample data
    from backend.app.scripts.seed_products import seed
    seed()

    # list products
    r = client.get("/products")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    # pick first product
    prod = data[0]
    product_id = prod["id"]

    # create an order for 1 unit
    r2 = client.post("/orders", json={"product_id": product_id, "quantity": 1})
    # Accept either 200 or 201 depending on implementation; ensure success
    assert r2.status_code in (200, 201)
    j = r2.json()
    assert "order_id" in j or j.get("status") == "created"
