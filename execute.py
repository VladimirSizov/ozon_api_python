# порядок выполнения
import upload_data as upload


# загрузка в БД

# в таблицу 'product_list'
upload.upd_product_list()

# в таблицы 'product_info',
upload.upd_product_info()

import db_connect as db
#db.execute("""DELETE FROM product_info WHERE product_id = 149801580""")