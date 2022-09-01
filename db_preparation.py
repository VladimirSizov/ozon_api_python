# создание таблиц в БД

from db_connect import *


# product_list
create_table_product_list = """
CREATE TABLE IF NOT EXISTS product_list (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	product_id INTEGER,
	offer_id TEXT
);
"""
execute_query(connection, create_table_product_list)


# product_info
create_table_product_info = """
CREATE TABLE IF NOT EXISTS product_info (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	product_id INTEGER,
	offer_id TEXT,
	visible INTEGER,
	images INTEGER
);
"""
execute_query(connection, create_table_product_info)