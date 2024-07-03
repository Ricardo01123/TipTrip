from re import match
from logging import getLogger, info
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Text, TextField, TextButton, ElevatedButton,
	Divider, Markdown, padding, margin, colors, icons, TextStyle, ScrollMode,
	ControlEvent
)

from resources.config import *
from resources.styles import *
from resources.functions import *
from components.titles import MainTitle
# from data import db
# from components.banners import ErrorBanner


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class SignInView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None
		self.btn_submit = None
		self.btn_sign_up = None

		self.txt_email: TextField = TextField(
			prefix_icon=icons.EMAIL,
			hint_text="Correo electrónico",
			**txt_style
		)

		self.txt_password: TextField = TextField(
			prefix_icon=icons.LOCK,
			hint_text="Contraseña",
			password=True,
			can_reveal_password=True,
			**txt_style
		)

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.btn_submit: ElevatedButton = ElevatedButton(
			width=self.page.width,
			content=Text(value="Iniciar sesión", size=BTN_TEXT_SIZE),
			on_click=self.btn_submit_clicked,
			**btn_primary_style
		)

		self.btn_sign_up: ElevatedButton = ElevatedButton(
			width=self.page.width,
			content=Text(value="Registrarse", size=BTN_TEXT_SIZE),
			on_click=lambda _: go_to_view(
				page=self.page,
				logger=logger,
				route="sign_up"
			),
			**btn_secondary_style,
		)

		# self.page.banner = ErrorBanner(page)

		return View(
			route="/",
			padding=padding.all(value=0.0),
			bgcolor=MAIN_COLOR,
			controls=[
				Container(
					content=Column(
						scroll=ScrollMode.HIDDEN,
						controls=[
							MainTitle(
								subtitle="Iniciar sesión",
								top_margin=(SPACING * 2),
					   		),
							Container(
								margin=margin.only(top=(SPACING * 4)),
								content=Column(
									spacing=(SPACING * 1.5),
									controls=[
										Container(
											height=TXT_CONT_SIZE,
											content=self.txt_email
										),
										Container(
											height=TXT_CONT_SIZE,
											content=self.txt_password
										),
										Container(
											content=TextButton(
												content=Container(
													content=Text(
														value="¿Olvidaste tu contraseña?",
														color=colors.BLACK
													)
												),
												on_click=lambda _: go_to_view(
													page=self.page,
													logger=logger,
													route="change_password"
												),
											)
										),
									]
								)
							),
							Container(
								margin=margin.only(top=(SPACING * 3)),
								content=Column(
									controls=[
										self.btn_submit,
										Divider(color=colors.TRANSPARENT),
										self.btn_sign_up
									]
								)
							),
							Container(
								margin=margin.only(top=(SPACING * 2)),
								content=Markdown(
									value=(
										"Para conocer más acerca de nuestra "
										"Política de Privacidad da click "
										"[aquí](https://www.google.com)."
									),
									code_style=TextStyle(
										color=colors.BLACK
									),
									on_tap_link=lambda _: go_to_view(
										page=self.page,
										logger=logger,
										route="privacy_politics"
									),
								)
							)
						]
					),
					**cont_main_style
				)
			]
		)

	def btn_submit_clicked(self, event: ControlEvent) -> None:
		info("Creando conexión a la base de datos...")
	# 	connection = db.connect_to_db()

		info("Verificando que el registro exista...")
	# 	conditions: dict = {
	# 		"username": self.txt_email.value,
	# 		"password": self.txt_password.value
	# 	}
	# 	record: list = db.get_record(connection, "users", conditions)
	#
	# 	if record is not None:
	# 		load_user_to_basket(self.basket, record)
	#
	# 		logger.info(
	# 			"Inicio de sesión correcto con credenciales: {}|{}"
	# 			.format(conditions["username"], conditions["password"])
	# 		)
	#
	# 		logger.info("Cerrando conexión con la base de datos...")
	# 		db.close_connection_to_db(connection)
	#
	# 		logger.info("Redirigiendo a la vista \"Inicio\" (\"/home\")...")
	# 		self.page.banner.close_banner(event)
	# 		self.page.go(f"/home/{self.txt_email.value}")
	#
	# 	else:
	# 		logger.info("Cerrando conexión con la base de datos...")
	# 		db.close_connection_to_db(connection)
	#
	# 		self.page.banner.set_content("Usuario y/o contraseña incorrectos")
	# 		self.page.banner.open_banner()
		go_to_view(page=self.page, logger=logger, route="home"),
