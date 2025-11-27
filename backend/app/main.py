from fastapi import FastAPI, HTTPException
from typing import List

from . import crud, db, models

app = FastAPI(title="Product Catalog API", version="0.1")

@app.on_event("startup")
def startup_event():
    """
    Initialize DB at application startup (convenience for local dev).
    In production, you'll run migrations separately.
    """
    db.init_db()

@app.get("/health")
def health():
    """
    Very small lightweight health-check. ALB / load balancer will use this.
    """
    return {"status": "ok"}

@app.get("/products", response_model=List[models.ProductOut])
def list_products():
    """
    Return list of products. Uses response_model to ensure consistent JSON schema.
    """
    return crud.get_products()

@app.get("/products/{product_id}", response_model=models.ProductOut)
def get_product(product_id: int):
    """
    Return a single product by id. If not found, return 404.
    """
    p = crud.get_product(product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p

@app.post("/products", response_model=models.ProductOut)
def create_product(payload: models.ProductIn):
    """
    Create product (dev/admin endpoint). Returns created product.
    """
    return crud.create_product(payload)

@app.post("/orders")
def create_order(payload: models.OrderIn):
    """
    Create an order: attempts to reserve stock and insert an order row.
    Returns 400 on insufficient stock.
    """
    order = crud.create_order(payload.product_id, payload.quantity)
    if not order:
        raise HTTPException(status_code=400, detail="Order failed (insufficient stock)")
    return {"order_id": order["id"], "status": "created"}
