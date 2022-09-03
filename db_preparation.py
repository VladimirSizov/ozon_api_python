# создание таблиц в БД

import db_connect as db


#db.execute("""PRAGMA foreign_keys=on""")

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
	product_id INTEGER PRIMARY KEY,
	offer_id TEXT,
	visible INTEGER DEFAULT FALSE,
	name TEXT,
	min_price INTEGER DEFAULT 0
);
""")

# images
db.execute("""
CREATE TABLE IF NOT EXISTS images (
	product_id INTEGER,
	image TEXT,
	FOREIGN KEY (product_id) REFERENCES product_info (product_id) ON DELETE CASCADE
);
""")
