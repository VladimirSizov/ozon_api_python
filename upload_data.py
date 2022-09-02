# загружаем в БД данные полученные по API
import api_connect as api
import db_connect as db
import db_preparation


def upd_product_list():
	# запрос 'v2/product/list'
	# в таблицу 'product_list'
	data = api.ApiSeller().post_product_list()['result']['items']
	for product in data:
		result = db.exec_fetch("SELECT product_id, offer_id FROM product_list WHERE product_id = :product_id AND offer_id = :offer_id", product)
		if not result:
			db.executemany("INSERT INTO product_list (product_id, offer_id) VALUES (:product_id, :offer_id);", [product])
			print('New data created: product_id: ' + str(product['product_id']) + ', offer_id: ' + str(product['offer_id']))
		else:
			print('Data is exist. product_id: ' + str(product['product_id']) + ', offer_id: ' + str(product['offer_id']))
	print("ALL DATA HAS BEEN WRITE IN 'product_list'\n")


def upd_product_info():
	# запрос 'v2/product/info'
	# таблицы 'product_info',
	# получаем product_id существующих записей в БД из 'product_list'
	result = db.exec_fetch("SELECT product_id FROM product_list;")
	for product in result:
		#  пробуем получить по данные по API
		try:
			data = api.ApiSeller().post_product_info(product[0])['result']

			product_id = data['id']
			offer_id = data['offer_id']
			visible = data['visible']
			images = data['images']
			name = data['name']
			min_price = data['price']

			values_write = [{
				'product_id': product_id,
				'offer_id': offer_id,
				'visible': visible,
				'name': name,
				'min_price': min_price
			}]
			# проверяем есть ли в 'product_info' запись по получкнному по API 'product_id' и 'offer_id'
			values_read = {'product_id': product_id, 'offer_id': offer_id,}
			query_read = "SELECT product_id, offer_id FROM product_info WHERE product_id = :product_id AND offer_id = :offer_id"
			result = db.exec_fetch(query_read, values_read)
			if not result:
				# записи с таким значением нет, делаем новую запись
				query_write = "INSERT INTO product_info (product_id, offer_id, visible) VALUES (:product_id, :offer_id, :visible);"
				db.executemany(query_write, values_write)
				print('New data created: product_id: ' + str(product_id) + ', offer_id: ' + str(offer_id))
			else:
				# запись есть, обновляем данные
				db.executemany("""UPDATE product_info
				SET name = :name
				WHERE product_id = :product_id AND offer_id = :offer_id""", values_write)
				print('Existing data updated. product_id: ' + str(product_id) + ', offer_id: ' + str(offer_id))

		except:
			# если записей по 'product_id' по запросу API не получили (удалены, не существует)
			print("Can't execute this PRODUCT is not exist. product_id: " + str(product[0]))
	print("ALL DATA HAS BEEN WRITE IN 'product_info'\n")
