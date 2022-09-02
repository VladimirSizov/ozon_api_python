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
			# если нет пары 'product_id' и 'offer_id', создаем новую запись
			db.executemany("INSERT INTO product_list (product_id, offer_id) VALUES (:product_id, :offer_id);", [product])
			print('New data created: product_id: ' + str(product['product_id']) + ', offer_id: ' + str(product['offer_id']))
		else:
			print('Data is exist. product_id: ' + str(product['product_id']) + ', offer_id: ' + str(product['offer_id']))
	print("ALL DATA HAS BEEN WRITE IN 'product_list'\n")


def upd_product_info():
	# запрос 'v2/product/info'
	# таблицы 'product_info', images
	# получаем product_id существующих записей в БД из 'product_list'
	result = db.exec_fetch("SELECT product_id FROM product_list;")
	for product in result:
		try:
			#  пробуем получить по данные по API
			data = api.ApiSeller().post_product_info(product[0])['result']
			product_id = data['id']
			offer_id = data['offer_id']
			visible = data['visible']
			new_images = data['images']
			name = data['name']
			min_price = float(data['min_price'])
			values_write = [{
				'product_id': product_id,
				'offer_id': offer_id,
				'visible': visible,
				'name': name,
				'min_price': min_price
			}]

			# проверяем есть ли в 'product_info' запись по полученному по API 'product_id' и 'offer_id'
			values_read = {'product_id': product_id, 'offer_id': offer_id,}
			query_read = "SELECT product_id, offer_id FROM product_info WHERE product_id = :product_id AND offer_id = :offer_id"
			result = db.exec_fetch(query_read, values_read)
			if not result:
				# в 'product_info' записи с таким значением нет, делаем новую запись
				db.executemany("""INSERT INTO product_info (
				product_id,
				offer_id,
				visible,
				name,
				min_price
				) VALUES (
				:product_id,
				:offer_id,
				:visible,
				:name,
				:min_price
				);""", values_write)
				#print('New data created: product_id: ' + str(product_id) + ', offer_id: ' + str(offer_id))
			else:
				# в 'product_info' запись есть, обновляем данные
				db.executemany("""UPDATE product_info
				SET
				name = :name,
				visible = :visible,
				min_price = :min_price
				WHERE product_id = :product_id AND offer_id = :offer_id""", values_write)
				#print('Existing data updated. product_id: ' + str(product_id) + ', offer_id: ' + str(offer_id))

			# проверяем есть ли в 'images' записи по полученному по API 'offer_id'
			#print('images')
			#print(images)
			old_images = db.exec_fetch("SELECT offer_id, image FROM images WHERE offer_id = :offer_id", [offer_id])
			if not old_images:
				# в 'images' записей с таким значением нет, делаем новую запись
				if new_images:
					for image in new_images:
						img_values = [{'offer_id': offer_id, 'image': image}]
						db.executemany("""INSERT INTO images (offer_id, image) VALUES (:offer_id, :image);""", img_values)
						print('new image add: '+ image)
			else:
				arr_old_images = []
				# в 'images' записи есть, обновляем данные
				for old_img in old_images:
					arr_old_images.append(old_img[1])
					if old_img[1] in new_images: #  если стар изобр есть в новых
						continue
					else:
						# удалить текущую старую запись из таблицы
						db.executemany("""DELETE FROM images WHERE image = :image""", [{'image': old_img[1]}])
						print('delete image: ' + old_img[1])
				for new_img in new_images:
					if new_img in arr_old_images:
						continue
					else:
						# записать новое изображение
						img_values = [{'offer_id': offer_id, 'image': new_img}]
						db.executemany("""INSERT INTO images (offer_id, image) VALUES (:offer_id, :image);""", img_values)
						print('new image add: ' + new_img)

		# если в 'product_info'записей по 'product_id' по запросу API не получили (удалены, не существует)
		except:
			print("Can't execute this PRODUCT is not exist. product_id: " + str(product[0]))


	print("ALL DATA HAS BEEN WRITE IN 'product_info'\n")
