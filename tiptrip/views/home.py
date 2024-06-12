import logging
from flet_route import Params, Basket
from flet import (
	Page, View, AppBar, Column, Row, Container, Text,
	IconButton, ElevatedButton, CrossAxisAlignment, MainAxisAlignment,
	ScrollMode, padding, icons, ControlEvent
)

from data import db
from resources.config import *
from resources.functions import clean_basket
from components.error_banner import ErrorBanner
from components.payment_input import PaymentInput
from components.address_input import AddressInput
from components.date_time_input import DateTimeInput
from components.gas_type_liters import GasLitersInput


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


class HomeView:
	def __init__(self):
		self.page = None
		self.params = None
		self.basket = None

		self.cont_gas_liters = None
		self.cont_address = None
		self.cont_date_time = None
		self.cont_payment = None

		self.btn_submit: ElevatedButton = ElevatedButton(
			text="Pagar",
			width=COMPONENTS_WIDTH,
			on_click=self.submit
		)

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.page.banner = ErrorBanner(page)

		self.cont_gas_liters = GasLitersInput(page)
		self.cont_address = AddressInput()
		self.cont_date_time = DateTimeInput(page)
		self.cont_payment = PaymentInput(page)

		return View(
			route="/home/:username",
			scroll=ScrollMode.AUTO,
			vertical_alignment=MainAxisAlignment.CENTER,
			horizontal_alignment=CrossAxisAlignment.CENTER,
			spacing=26,
			controls=[
				AppBar(
					leading=IconButton(
						icon=icons.VERIFIED_USER,
					),
					title=Text(value=basket.get("username")),
					actions=[
						IconButton(
							icon=icons.LOGOUT,
							on_click=self.sign_out
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
								ElevatedButton(
									text="Ver historial de pedidos",
									width=COMPONENTS_WIDTH,
									visible=(
										False
										if self.basket.get("role") == "user"
										else True
									),
									on_click=lambda _: self.page.go("/history")
								)
							),
							Container(
								ElevatedButton(
									text="Dar de alta nuevo administrador",
									width=COMPONENTS_WIDTH,
									visible=(
										False
										if self.basket.get("role") == "user"
										else True
									),
									on_click=lambda _: self.page.go("/sign_up")
								)
							),
							Container(
								content=Text(
									value="Comprar gas",
									size=TITLE_SIZE
								)
							),
							self.cont_gas_liters,
							self.cont_address,
							self.cont_date_time,
							self.cont_payment,
							Container(
								padding=padding.only(bottom=EXTERIOR_PADDING),
								content=self.btn_submit
							)
						]
					)
				)
			]
		)

	def sign_out(self, event: ControlEvent):
		logging.info("Cerrando sesión...")
		self.page.banner.close_banner(event)
		clean_basket(self.basket)
		self.page.go('/')

	def get_all_values(self) -> dict:
		values: dict = {
			"gas_type": self.cont_gas_liters.get_gas_type(),
			"liters_quantity": self.cont_gas_liters.get_liters_quantity(),
			"total": self.cont_gas_liters.get_total(),
			"street": self.cont_address.get_street(),
			"colony": self.cont_address.get_colony(),
			"municipality": self.cont_address.get_municipality(),
			"cp": self.cont_address.get_cp(),
			"state": self.cont_address.get_state(),
			"date": self.cont_date_time.get_deliver_date(),
			"hour": self.cont_date_time.get_deliver_time(),
			"payment_method": self.cont_payment.get_payment_method()
		}

		if values["payment_method"] == "card":
			values["card_number"] = self.cont_payment.card_payment_input.get_card_number()
			values["expiration_date"] = self.cont_payment.card_payment_input.get_card_expiration_date()
			values["cvc"] = self.cont_payment.card_payment_input.get_card_cvc()
			values["cardholder"] = self.cont_payment.card_payment_input.get_cardholder()
		else:
			values["card_number"] = None
			values["expiration_date"] = None
			values["cvc"] = None
			values["cardholder"] = None

		return values

	def validate(self) -> bool:
		values: dict = self.get_all_values()

		logging.info("Validando que todos los campos contengan un valor...")
		for key, value in values.items():
			if values["payment_method"] == "card" and value is None:
				return False

		return True

	def submit(self, event: ControlEvent) -> None:
		logger.info("Creando conexión a la base de datos...")
		connection = db.connect_to_db()

		if self.validate():
			values: list = [value for key, value in self.get_all_values().items()]
			values.insert(0, self.basket.get("user_id"))

			logging.info("Insertando pedido en la base de datos...")
			db.insert_record(connection, "orders", values)
			last_id = db.get_last_id(connection, "orders")

			logger.info("Cerrando conexión con la base de datos...")
			db.close_connection_to_db(connection)

			self.page.banner.close_banner(event)
			self.page.go(f"/paid/{last_id}")
		else:
			logger.info("Cerrando conexión con la base de datos...")
			db.close_connection_to_db(connection)

			self.page.banner.set_content("Campos requeridos vacíos")
			self.page.banner.open_banner()
