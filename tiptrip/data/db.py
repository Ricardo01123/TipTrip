import os
import logging
import sqlite3 as sql
from sqlite3 import Connection, Cursor

from resources.config import PROJECT_NAME, DB_PATH, ADMIN_VALUES


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


def initialize_db() -> None:
	try:
		logger.info("Iniciando conexión...")
		connection: Connection = connect_to_db()

		logger.info("Iniciando cursor...")
		cursor: Cursor = connection.cursor()

		logger.info("Iniciando tablas...")
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				username TEXT NOT NULL UNIQUE,
				password TEXT NOT NULL,
				role TEXT NOT NULL
			)
		""")
		logger.info("Tabla \"users\" creada correctamente")

		cursor.execute("""
			CREATE TABLE IF NOT EXISTS orders (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_id INTEGER NOT NULL,
				gas_type TEXT NOT NULL,
				liters_quantity INTEGER NOT NULL,
				total REAL NOT NULL,
				street TEXT NOT NULL,
				colony TEXT NOT NULL,
				municipality TEXT NOT NULL,
				cp INTEGER NOT NULL,
				state TEXT NOT NULL,
				date TEXT NOT NULL,
				hour TEXT NOT NULL,
				payment_method TEXT NOT NULL,
				card_number INTEGER,
				expiration_date TEXT,
				cvc INTEGER,
				cardholder TEXT,
				FOREIGN KEY (user_id) REFERENCES users(id)
			)
		""")
		logger.info("Tabla \"orders\" creada correctamente")

		logger.info("Creando usuario administrador...")
		create_admin(connection)

		logger.info("Guardando cambios y cerrando conexión...")
		connection.commit()
		cursor.close()
		connection.close()

	except Exception as e:
		logger.error(
			"Ocurrió un error al iniciar la base de datos: {}"
			.format(e)
		)


def connect_to_db() -> Connection:
	try:
		connection: Connection = sql.connect(DB_PATH)
		return connection

	except Exception as e:
		logger.error(
			"Ocurrió un error al crear la conexión con la base de datos: {}"
			.format(e)
		)


def insert_record(connection: Connection, table: str, values: list) -> None:
	try:
		cursor: Cursor = connection.cursor()
		if table == "users":
			cursor.execute(
				"""
					INSERT INTO users (username, password, role)
					VALUES (?, ?, ?)
				""",
				values
			)

		elif table == "orders":
			cursor.execute(
				"""
					INSERT INTO orders (
						user_id,
						gas_type,
						liters_quantity,
						total,
						street,
						colony,
						municipality,
						cp,
						state,
						date,
						hour,
						payment_method,
						card_number,
						expiration_date,
						cvc,
						cardholder
					)
					VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				""",
				values
			)
		connection.commit()
		cursor.close()

	except Exception as e:
		logger.error(
			"Ocurrió un error al insertar los datos {} "
			"en la base de datos: {}"
			.format(values, e)
		)


def get_record(connection: Connection, table: str, conditions: dict) -> list:
	try:
		cursor: Cursor = connection.cursor()

		cons_str = [f"{cond} = ?" for cond in conditions.keys()]
		values = list(conditions.values())
		query = f"SELECT * FROM {table} WHERE {' AND '.join(cons_str)}"

		record: Cursor = cursor.execute(query, values)
		result: list = [row for row in record][0]

		cursor.close()
		return result

	except Exception as e:
		logger.error(
			"Ocurrió un error al obtener el registro {} de la base de datos: {}"
			.format(conditions, e)
		)


def get_all_records(connection: Connection, table: str) -> list:
	try:
		cursor: Cursor = connection.cursor()
		sentence: Cursor = cursor.execute(f"SELECT * FROM {table}")
		data: list = [row for row in sentence]
		return data

	except Exception as e:
		logger.error(
			"Ocurrió un error al obtener todos los registros "
			"de la base de datos: {}"
			.format(e)
		)


def get_last_id(connection: Connection, table: str) -> int:
	try:
		cursor: Cursor = connection.cursor()

		cursor.execute(f"SELECT MAX(id) FROM {table}")
		result: int = cursor.fetchone()[0]

		cursor.close()
		return result

	except Exception as e:
		logger.error(
			"Ocurrió un error al obtener el último id de la tabla {} "
			"de la base de datos: {}"
			.format(table, e)
		)


def is_table_empty(connection: Connection, table: str) -> bool:
	try:
		cursor: Cursor = connection.cursor()
		cursor.execute(f"SELECT COUNT(*) FROM {table}")
		count: int = cursor.fetchone()[0]

		cursor.close()
		return count == 0

	except Exception as e:
		logger.error(
			"Ocurrió un error al revisar si la tabla {} está vacía: {}"
			.format(table, e)
		)


def close_connection_to_db(connection: Connection) -> None:
	try:
		connection.close()

	except Exception as e:
		logger.error(
			"Ocurrió un error al cerrar la conexión con la base de datos: {}"
			.format(e)
		)


def create_admin(connection: Connection) -> None:
	try:
		conditions: dict = {
			"username": ADMIN_VALUES[0],
			"password": ADMIN_VALUES[1]
		}
		if is_table_empty(connection, "users"):
			cursor: Cursor = connection.cursor()
			cursor.execute(
				"INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
				ADMIN_VALUES
			)
			connection.commit()
			cursor.close()

	except Exception as e:
		logger.error(
			"Ocurrió un error al insertar el registro administrador {} "
			"en la base de datos: {}"
			.format(ADMIN_VALUES, e)
		)


def clear_db(connection: Connection, table: str) -> None:
	try:
		cursor: Cursor = connection.cursor()
		cursor.execute(f"DELETE FROM {table}")
		connection.commit()
		cursor.close()

	except Exception as e:
		logger.error(
			"Ocurrió un error al borrar todos los registros "
			"de la tabla {} de la base de datos: {}"
			.format(table, e)
		)
