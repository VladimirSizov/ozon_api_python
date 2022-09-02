# создание таблиц в БД

import db_connect as db


# product_list
db.execute("""
CREATE TABLE IF NOT EXISTS product_list (
	product_id INTEGER,
	offer_id TEXT
);
""")


# product_info
db.execute("""
CREATE TABLE IF NOT EXISTS product_info (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	product_id INTEGER,
	offer_id TEXT,
	visible INTEGER DEFAULT FALSE,
	images TEXT DEFAULT 0,
	name TEXT,
	min_price REAL DEFAULT 0
);
""")
