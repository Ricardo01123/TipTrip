import os
import sqlite3 as sql

from resources.config import DB_PATH


def initialize_db() -> None:
	connection = sql.connect(DB_PATH)
	cursor = connection.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS users (
			username TEXT NOT NULL,
			password TEXT NOT NULL
		)
	""")
	connection.commit()
	cursor.close()
	connection.close()


def connect_to_db():
	connection = sql.connect(DB_PATH)
	return connection


def close_connection_to_db(connection) -> None:
	connection.close()


def check_record_exists(
		connection, values: str | tuple) -> bool:
	cursor = connection.cursor()

	if isinstance(values, str):
		cursor.execute(
			"SELECT COUNT(*) FROM users WHERE username = ?",
			(values, )
		)
	else:
		cursor.execute(
			"SELECT COUNT(*) FROM users WHERE username = ? and password = ?",
			values
		)
	result = cursor.fetchone()[0] > 0
	cursor.close()
	return result


def insert_record(connection, values: tuple) -> None:
	cursor = connection.cursor()
	cursor.execute(
		"INSERT INTO users VALUES (?, ?)",
		values
	)
	connection.commit()
	cursor.close()


def get_password(connection, username) -> str:
	cursor = connection.cursor()
	record: str = cursor.execute(
		"SELECT * FROM users WHERE username = ?",
		(username, )
	)
	result = [row for row in record]
	cursor.close()
	return result[0][1]


def get_all_records(connection) -> list:
	cursor = connection.cursor()
	sentence = cursor.execute("SELECT * FROM users")
	data = [row for row in sentence]
	return data


def clear_db(connection) -> None:
	cursor = connection.cursor()
	cursor.execute("DELETE FROM users")
	connection.commit()
	cursor.close()
