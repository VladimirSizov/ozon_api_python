import sqlite3
from sqlite3 import Error


def create_connection(path):
	"""подключение к БД"""
	connection = None
	try:
		connection = sqlite3.connect(path)
		print("Connection SQLite DB successful.")
	except Error as e:
		print(f"The error '{e}' occurred.")
	return connection

# создаем соединение с БД
connection = create_connection("db.sqlite3")


def execute_query(connection, query):
	"""запись в БД"""
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		connection.commit()
		print("Query executed successfully.")
	except Error as e:
		print(f"The error '{e}' occurred.")

def executemany_query(connection, query, values):
	"""запись в БД"""
	cursor = connection.cursor()
	try:
		cursor.executemany(query, values)
		connection.commit()
		print("Query executed successfully.")
	except Error as e:
		print(f"The error '{e}' occurred.")


def execute_read_query(connection, query, values):
	"""извлечение из БД"""
	cursor = connection.cursor()
	result = None
	try:
		cursor.execute(query, values)
		result = cursor.fetchall()
		return result
	except Error as e:
		print(f"The error '{e}' occurred.")
