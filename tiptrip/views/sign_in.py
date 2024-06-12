import logging
from flet_route import Params, Basket
from flet import (
	Page, View, AppBar, Column, Row, Container, Banner,
	Text, TextField, TextButton, ElevatedButton,
	MainAxisAlignment, TextAlign, padding,
	ControlEvent,
	colors, Icon, icons
)

from data import db
from resources.config import *
from components.error_banner import ErrorBanner
from resources.functions import load_user_to_basket


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


class SignInView:
	def __init__(self):
		self.page = None
		self.params = None
		self.basket = None

		self.txt_username: TextField = TextField(
			label="Nombre de usuario",
			text_align=TextAlign.LEFT,
			width=COMPONENTS_WIDTH,
			on_change=self.validate
		)
		self.txt_password: TextField = TextField(
			label="Contraseña",
			text_align=TextAlign.LEFT,
			width=COMPONENTS_WIDTH,
			password=True,
			on_change=self.validate
		)
		self.btn_submit: ElevatedButton = ElevatedButton(
			text="Iniciar sesión",
			width=COMPONENTS_WIDTH,
			disabled=True,
			on_click=self.submit
		)

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.page.banner = ErrorBanner(page)

		return View(
			route='/',
			controls=[
				Container(
					width=APP_WIDTH,
					height=APP_HEIGHT - (APP_BAR_HEIGHT * 2),
					padding=padding.only(
						left=EXTERIOR_PADDING,
						right=EXTERIOR_PADDING
					),
					content=Column(
						alignment=MainAxisAlignment.SPACE_EVENLY,
						controls=[
							Container(
								content=Text(
									value=PROJECT_NAME,
									size=PROJECT_NAME_SIZE
								)
							),
							Container(
								content=Text(
									value="Iniciar sesión",
									size=TITLE_SIZE
								)
							),
							Container(content=self.txt_username),
							Container(content=self.txt_password),
							Container(content=self.btn_submit),
							Row(
								width=COMPONENTS_WIDTH,
								alignment=MainAxisAlignment.SPACE_BETWEEN,
								controls=[
									Container(
										TextButton(
											text="Crear cuenta",
											on_click=lambda _:
											self.page.go("/sign_up")
										)
									),
									Container(
										TextButton(
											text="Olvidé mi contraseña",
											on_click=lambda _:
											self.page.go("/forgotten_pwd")
										),
									)
								]
							)
						]
					)
				)
			]
		)

	def validate(self, event: ControlEvent) -> None:
		if all([self.txt_username.value, self.txt_password.value]):
			self.btn_submit.disabled = False
		else:
			self.btn_submit.disabled = True
		self.page.update()

	def submit(self, event: ControlEvent) -> None:
		logger.info("Creando conexión a la base de datos...")
		connection = db.connect_to_db()

		logger.info("Verificando que el registro exista...")
		conditions: dict = {
			"username": self.txt_username.value,
			"password": self.txt_password.value
		}
		record: list = db.get_record(connection, "users", conditions)

		if record is not None:
			load_user_to_basket(self.basket, record)

			logger.info(
				"Inicio de sesión correcto con credenciales: {}|{}"
				.format(conditions["username"], conditions["password"])
			)

			logger.info("Cerrando conexión con la base de datos...")
			db.close_connection_to_db(connection)

			logger.info("Redirigiendo a la vista \"Inicio\" (\"/home\")...")
			self.page.banner.close_banner(event)
			self.page.go(f"/home/{self.txt_username.value}")

		else:
			logger.info("Cerrando conexión con la base de datos...")
			db.close_connection_to_db(connection)

			self.page.banner.set_content("Usuario y/o contraseña incorrectos")
			self.page.banner.open_banner()

