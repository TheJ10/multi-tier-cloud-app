from . import db

def get_products():
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, stock, description FROM products")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "price": r[2], "stock": r[3], "description": r[4]} for r in rows]

def get_product(product_id: int):
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, stock, description FROM products WHERE id = ?", (product_id,))
    r = cur.fetchone()
    conn.close()
    if not r:
        return None
    return {"id": r[0], "name": r[1], "price": r[2], "stock": r[3], "description": r[4]}

def create_product(payload):
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, price, stock, description) VALUES (?, ?, ?, ?)",
                (payload.name, payload.price, payload.stock, getattr(payload, "description", None)))
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return get_product(pid)

def create_order(product_id: int, quantity: int):
    conn = db.get_conn()
    cur = conn.cursor()
    # simple concurrency-safe approach for sqlite in dev: check stock, update, insert within same connection
    cur.execute("SELECT stock FROM products WHERE id = ?", (product_id,))
    r = cur.fetchone()
    if not r or r[0] < quantity:
        conn.close()
        return None
    new_stock = r[0] - quantity
    cur.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))
    cur.execute("INSERT INTO orders (product_id, quantity) VALUES (?, ?)", (product_id, quantity))
    conn.commit()
    oid = cur.lastrowid
    conn.close()
    return {"id": oid}
