import sqlite3
from paths import DB_PATH


class DB:
    """Удобная обёртка над sqlite3. Все запросы — параметризованные."""

    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(str(path))
        self.conn.row_factory = sqlite3.Row

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def execute(self, query, params=()):
        return self.conn.execute(query, params)

    def fetchone(self, query, params=()):
        return self.conn.execute(query, params).fetchone()

    def fetchall(self, query, params=()):
        return self.conn.execute(query, params).fetchall()

    def insert(self, query, params=()):
        cur = self.conn.execute(query, params)
        self.conn.commit()
        return cur.lastrowid