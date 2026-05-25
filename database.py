import sqlite3
import os
from kivy.utils import platform


def _db_path():
    if platform == 'android':
        try:
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), 'omborxona.db')
        except Exception:
            pass
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'omborxona.db')


class Database:
    def __init__(self):
        self.path = _db_path()
        self._init()

    def _con(self):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        return con

    def _init(self):
        with self._con() as c:
            c.executescript("""
                CREATE TABLE IF NOT EXISTS products (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    name       TEXT    NOT NULL,
                    price      REAL    NOT NULL DEFAULT 0,
                    quantity   INTEGER NOT NULL DEFAULT 0,
                    image_path TEXT    NOT NULL DEFAULT ''
                );
                CREATE TABLE IF NOT EXISTS sales (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id   INTEGER NOT NULL,
                    product_name TEXT    NOT NULL,
                    quantity     INTEGER NOT NULL,
                    unit_price   REAL    NOT NULL,
                    total_price  REAL    NOT NULL,
                    sold_at      DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """)

    # ── Products ──────────────────────────────────────────────────────────────

    def get_products(self, search=''):
        with self._con() as c:
            rows = c.execute(
                "SELECT id, name, price, quantity, image_path "
                "FROM products WHERE name LIKE ? ORDER BY name",
                (f'%{search}%',)
            ).fetchall()
        return [tuple(r) for r in rows]

    def add_product(self, name, price, image_path=''):
        with self._con() as c:
            cur = c.execute(
                "INSERT INTO products (name, price, image_path) VALUES (?, ?, ?)",
                (name.strip(), float(price), image_path)
            )
            return cur.lastrowid

    def set_quantity(self, product_id, qty):
        with self._con() as c:
            c.execute(
                "UPDATE products SET quantity = ? WHERE id = ?",
                (max(0, int(qty)), product_id)
            )

    def add_quantity(self, product_id, amount):
        with self._con() as c:
            c.execute(
                "UPDATE products SET quantity = quantity + ? WHERE id = ?",
                (max(0, int(amount)), product_id)
            )

    # ── Sales ─────────────────────────────────────────────────────────────────

    def process_sale(self, cart):
        """cart = {pid: {'name':str, 'price':float, 'qty':int}}"""
        with self._con() as c:
            for pid, item in cart.items():
                q, p = int(item['qty']), float(item['price'])
                c.execute(
                    "INSERT INTO sales(product_id,product_name,quantity,unit_price,total_price)"
                    " VALUES(?,?,?,?,?)",
                    (pid, item['name'], q, p, q * p)
                )
                c.execute(
                    "UPDATE products SET quantity = MAX(0, quantity - ?) WHERE id = ?",
                    (q, pid)
                )

    def get_stats(self):
        with self._con() as c:
            rows = c.execute(
                "SELECT product_name, SUM(quantity) as qty, SUM(total_price) as revenue "
                "FROM sales GROUP BY product_name ORDER BY revenue DESC"
            ).fetchall()
        return [tuple(r) for r in rows]

    def get_total_revenue(self):
        with self._con() as c:
            return c.execute(
                "SELECT COALESCE(SUM(total_price), 0) FROM sales"
            ).fetchone()[0]

    def clear_stats(self):
        with self._con() as c:
            c.execute("DELETE FROM sales")
