import logging
from flet_route import Params, Basket

from flet import (
	Page, View, Container, AppBar, Column,
	Text, IconButton, ElevatedButton, padding, icons,
	MainAxisAlignment, CrossAxisAlignment, ScrollMode, ControlEvent
)

from data import db
from resources.functions import clean_basket

from resources.config import (
	TITLE_SIZE, TEXT_SIZE, PROJECT_NAME, PROJECT_NAME_SIZE,
	APP_WIDTH, EXTERIOR_PADDING, COMPONENTS_WIDTH
)


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


class PaidView:
	def __init__(self):
		self.page = None
		self.params = None
		self.basket = None

		self.order = None
		self.lbl_gas_type = None
		self.lbl_payment_method = None
		self.lbl_card_number = None
		self.lbl_expiration_date = None
		self.lbl_cvc = None
		self.lbl_cardholder = None

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.order: list = self.get_order()
		self.lbl_gas_type: Text = Text(
			value=(
				"Tipo de gas: Gas estacionario"
				if self.order[2] == "stationary"
				else "Tipo de gas: Tanque de gas"
			),
			size=TEXT_SIZE
		)
		self.lbl_payment_method: Text = Text(
			value=(
				"Método de pago: Efectivo"
				if self.order[12] == "cash"
				else "Método de pago: Tarjeta de crédito/débito"
			),
			size=TEXT_SIZE
		)
		self.lbl_card_number: Text = Text(
			value=f"Tarjeta de pago: {self.order[13]}",
			size=TEXT_SIZE,
			visible=(
				True
				if self.order[12] == "card"
				else False
			)
		)
		self.lbl_expiration_date: Text = Text(
			value=f"Fecha de expiración: {self.order[14]}",
			size=TEXT_SIZE,
			visible=(
				True
				if self.order[12] == "card"
				else False
			)
		)
		self.lbl_cvc: Text = Text(
			value=f"CVC: {self.order[15]}",
			size=TEXT_SIZE,
			visible=(
				True
				if self.order[12] == "card"
				else False
			)
		)
		self.lbl_cardholder: Text = Text(
			value=f"Dueño de la tarjeta: {self.order[15]}",
			size=TEXT_SIZE,
			visible=(
				True
				if self.order[12] == "card"
				else False
			)
		)

		return View(
			route="/paid/:last_order_id",
			scroll=ScrollMode.AUTO,
			vertical_alignment=MainAxisAlignment.CENTER,
			horizontal_alignment=CrossAxisAlignment.CENTER,
			controls=[
				AppBar(
					leading=IconButton(
						icon=icons.VERIFIED_USER,
					),
					title=Text(value=basket.get("username")),
					actions=[
						IconButton(
							icon=icons.LOGOUT,
							on_click=lambda _: self.sign_out
						)
					]
				),
				Container(
					width=APP_WIDTH,
					padding=padding.only(
						left=EXTERIOR_PADDING,
						right=EXTERIOR_PADDING
					),
					content=Column(
						alignment=MainAxisAlignment.START,
						spacing=30,
						controls=[
							Container(
								content=Text(
									value=PROJECT_NAME,
									size=PROJECT_NAME_SIZE
								)
							),
							Container(
								content=Text(
									value="Resumen de pedido",
									size=TITLE_SIZE
								)
							),
							self.lbl_gas_type,
							Text(
								value=f"Cantidad de litros: {self.order[3]}",
								size=TEXT_SIZE
							),
							Text(
								value=f"Total a pagar: ${self.order[4]}",
								size=TEXT_SIZE
							),
							Text(
								value=f"Calle: {self.order[5]}",
								size=TEXT_SIZE
							),
							Text(
								value=f"Colonia: {self.order[6]}",
								size=TEXT_SIZE
							),
							Text(
								value=f"Municipio: {self.order[7]}",
								size=TEXT_SIZE
							),
							Text(
								value=f"Código postal: {self.order[8]}",
								size=TEXT_SIZE
							),
							Text(
								value=f"Estado: {self.order[9]}",
								size=TEXT_SIZE
							),
							Text(
								value=f"Fecha de entrega: {self.order[10]}",
								size=TEXT_SIZE
							),
							Text(
								value=f"Hora de entrega: {self.order[11]}",
								size=TEXT_SIZE
							),
							self.lbl_payment_method,
							self.lbl_card_number,
							self.lbl_expiration_date,
							self.lbl_cvc,
							self.lbl_cardholder,
							Container(
								padding=padding.only(bottom=EXTERIOR_PADDING),
								content=ElevatedButton(
									text="Regresar",
									width=COMPONENTS_WIDTH,
									on_click=lambda _: self.page.go(f"/home/{self.basket.get('username')}")
								)
							)
						]
					)
				)
			]
		)

	def get_order(self) -> list:
		logger.info("Creando conexión a la base de datos...")
		connection = db.connect_to_db()

		logger.info("Obteniendo pedido de la base de datos...")
		conditions: dict = {
			"id": self.params.get("last_order_id"),
			"user_id": self.basket.get("user_id")
		}

		order = db.get_record(connection, "orders", conditions)

		logger.info("Cerrando conexión con la base de datos...")
		db.close_connection_to_db(connection)

		return order

	def sign_out(self, event: ControlEvent):
		logging.info("Cerrando sesión...")
		self.page.banner.close_banner(event)
		clean_basket(self.basket)
		self.page.go('/')
