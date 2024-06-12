import logging
from flet import DataTable, DataColumn, DataRow, DataCell, Text

from data import db
from resources.config import PROJECT_NAME


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


def get_data() -> list:
	logger.info("Creando conexión a la base de datos...")
	connection = db.connect_to_db()

	logger.info("Obteniendo todos los registros de pedidos...")
	data: list = db.get_all_records(connection, "orders")

	result: list = []

	for record in data:
		user: str = db.get_record(connection, "users", {"id": record[1]})[1]
		gas_type: str = (
			"Gas estacionario"
			if record[2] == "stationary"
			else "Tanque de gas"
		)
		payment_method: str = (
			"Efectivo"
			if record[12] == "cash"
			else "Tarjeta de crédito/débito"
		)
		card_number: int | str = (
			record[13]
			if record[12] == "card"
			else ""
		)
		expiration_date: str = (
			record[14]
			if record[12] == "card"
			else ""
		)
		cvc: int | str = (
			record[15]
			if record[12] == "card"
			else ""
		)
		cardholder: str = (
			record[16]
			if record[12] == "card"
			else ""
		)

		row: DataRow = DataRow(
			cells=[
				DataCell(Text(value=user)),
				DataCell(Text(value=gas_type)),
				DataCell(Text(value=record[3])),
				DataCell(Text(value=record[4])),
				DataCell(Text(value=record[5])),
				DataCell(Text(value=record[6])),
				DataCell(Text(value=record[7])),
				DataCell(Text(value=record[8])),
				DataCell(Text(value=record[9])),
				DataCell(Text(value=record[10])),
				DataCell(Text(value=record[11])),
				DataCell(Text(value=payment_method)),
				DataCell(Text(value=card_number)),
				DataCell(Text(value=expiration_date)),
				DataCell(Text(value=cvc)),
				DataCell(Text(value=cardholder)),
			]
		)

		result.append(row)

	logger.info("Cerrando conexión con la base de datos...")
	db.close_connection_to_db(connection)

	return result


class HistoryTable(DataTable):
	def __init__(self):
		super().__init__()

		self.show_bottom_border = True,
		self.columns = [
			DataColumn(Text(value="Usuario")),
			DataColumn(Text(value="Tipo de gas")),
			DataColumn(Text(value="Litros"), numeric=True),
			DataColumn(Text(value="Total a pagar ($)"), numeric=True),
			DataColumn(Text(value="Calle")),
			DataColumn(Text(value="Colonia")),
			DataColumn(Text(value="Municipio")),
			DataColumn(Text(value="Código postal"), numeric=True),
			DataColumn(Text(value="Estado")),
			DataColumn(Text(value="Fecha de entrega")),
			DataColumn(Text(value="Hora de entrega")),
			DataColumn(Text(value="Método de pago")),
			DataColumn(Text(value="Tarjeta")),
			DataColumn(Text(value="Fecha de expiración")),
			DataColumn(Text(value="CVC")),
			DataColumn(Text(value="Dueño de la tarjeta")),
		]

		self.rows = get_data()
