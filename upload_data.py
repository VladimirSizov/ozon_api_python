# загружаем в БД данные полученные по API
import api_connect as api
import db_connect as db
import db_preparation


def upd_product_list():
	# запрос 'v2/product/list'
	# в таблицу 'product_list'
	data = api.ApiSeller().post_product_list()['result']['items']
	for product in data:
		query_read = "SELECT product_id, offer_id FROM product_list WHERE product_id = :product_id AND offer_id = :offer_id"
		result = db.execute_read_query(db.connection, query_read, product)
		if not result:
			query_write = "INSERT INTO product_list (product_id, offer_id) VALUES (:product_id, :offer_id);"
			db.executemany_query(db.connection, query_write, [product])
			print('New write: product_id: ' + str(product['product_id']) + ', offer_id: ' + str(product['offer_id']))
	print("All data has ben write in table 'product_list'.")


def upd_product_info():
	# запрос 'v2/product/info'
	# таблицы 'product_info',
	# получаем существующие записи из 'product_info'
	query_read = "SELECT product_id FROM product_list;"
	result = db.execute_read_query(db.connection, query_read, {})
	for product in result:
		try:
			data = api.ApiSeller().post_product_info(product[0])['result']
			product_id = data['id']
			offer_id = data['offer_id']
			# проверяем
			query_read = "SELECT product_id, offer_id FROM product_info WHERE product_id = :product_id AND offer_id = :offer_id"
			result = db.execute_read_query(db.connection, query_read, {'product_id': product_id, 'offer_id': offer_id})
			if not result:
				# записи с таким значением нет, делаем новую запись
				query_write = "INSERT INTO product_info (product_id, offer_id) VALUES (:product_id, :offer_id);"
				db.executemany_query(db.connection, query_write, [{'product_id': product_id, 'offer_id': offer_id}])
				print('New write: product_id: ' + str(product_id) + ', offer_id: ' + str(offer_id))
		except:
			print("Can't execute product_id: " + str(product[0]) + ', this PRODUCT is not exist.')
	print("All data has ben write in table 'product_info'.")