import api_connect as api
import db_connect as db
import db_preparation

def upd_product_list():
	# получаем данные
	data = api.ApiSeller().post_product_list()['result']['items']
	for product in data:
		product_id = product['product_id']
		offer_id = product['offer_id']
		# проверяем есть ли product_id
		query_read = "SELECT offer_id FROM product_list WHERE product_id = ?;"
		result = db.execute_read_query(db.connection, query_read, [product_id])
		exist_offer_id = []
		for item in result:
			offer_id = item[0]
			exist_offer_id.append(offer_id)
		# если в БД нет пары (product_id, offer_id)
		if exist_offer_id.count(offer_id) == 0:
			# записываем новое значение
			query_write = "INSERT INTO product_list (product_id, offer_id) VALUES (:product_id, :offer_id);"
			result = db.executemany_query(db.connection, query_write, [product])
			print('New write: ', product)
