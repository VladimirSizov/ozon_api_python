# создание таблиц в БД

from db_connect import *

# product_list
create_table_product_list = """
CREATE TABLE IF NOT EXISTS product_list (
	product_id INTEGER,
	offer_id TEXT
);
"""
execute_query(connection, create_table_product_list)
