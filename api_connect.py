# получение данных по API с OZON
import my
import requests
import json


class ApiSeller():
	"""получение данных по API"""

	def __init__(self):
		self.client_Id = my.client_Id # ваш Client-Id
		self.api_key = my.api_key # ваш Api-Key
		self.url = 'https://api-seller.ozon.ru/'


	def request(self, method_url, body={}):
		"""запрос по API"""
		url = self.url + method_url
		headers = {'Client-Id': self.client_Id, 'Api-Key': self.api_key}
		response = requests.post(url, headers=headers, data=json.dumps(body))
		return json.loads(response.text)


	def post_product_list(self):
		"""Список товаров
		https://docs.ozon.ru/api/seller/#operation/ProductAPI_GetProductList"""
		method_url = 'v2/product/list'
		return self.request(method_url)


	def post_product_info(self, product_id):
		"""Информация о товаре (только по одному product_id)
		https://docs.ozon.ru/api/seller/#operation/ProductAPI_GetProductInfoV2"""
		method_url = 'v2/product/info'
		body = {"product_id": product_id}
		return self.request(method_url, body)
