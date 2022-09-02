# создание таблиц в БД

import db_connect as db


# product_list
db.execute("""
CREATE TABLE IF NOT EXISTS product_list (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
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
	name TEXT,
	min_price INTEGER DEFAULT 0
);
""")

# images
db.execute("""
CREATE TABLE IF NOT EXISTS images (
	offer_id TEXT,
	image TEXT,
	FOREIGN KEY (offer_id) REFERENCES product_info (offer_id) ON DELETE CASCADE
);
""")
