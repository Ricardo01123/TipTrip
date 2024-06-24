from re import match
from logging import getLogger, info
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Banner, Text, TextField, TextButton,
	ElevatedButton, Divider, Markdown, padding, margin, colors, icons,
	ControlEvent
)

# from data import db
from resources.config import *
from resources.functions import *
from components.titles import MainTitleColumn
from resources.styles import (
	cont_main_style, txt_style, btn_primary_style, btn_secondary_style
)
# from components.banners import ErrorBanner


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class SignInView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.txt_email: TextField = TextField(
			prefix_icon=icons.EMAIL,
			hint_text="Correo electrónico",
			on_change=self.validate,
			**txt_style
		)

		self.txt_password: TextField = TextField(
			prefix_icon=icons.LOCK,
			hint_text="Contraseña",
			password=True,
			can_reveal_password=True,
			on_change=self.validate,
			**txt_style
		)

		self.btn_submit: ElevatedButton = ElevatedButton(
			text="Iniciar sesión",
			on_click=self.btn_submit_clicked,
			on_hover=main_btn_hover,
			**btn_primary_style
		)

		self.btn_sign_up: ElevatedButton = ElevatedButton(
			text="Registrarse",
			on_hover=secondary_btn_hover,
			on_click=lambda _: go_to_view(
				page=self.page,
				logger=logger,
				route="sign_up"
			),
			**btn_secondary_style,
		)

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		# self.page.banner = ErrorBanner(page)

		return View(
			route="/",
			padding=padding.all(value=0.0),
			bgcolor=MAIN_COLOR,
			controls=[
				Container(
					content=Column(
						controls=[
							MainTitleColumn(
								subtitle="Iniciar sesión",
								top_margin=(SPACING * 2)
							),
							Container(
								margin=margin.only(top=(SPACING * 3)),
								content=Column(
									spacing=SPACING,
									controls=[
										Container(content=self.txt_email),
										Container(content=self.txt_password),
										TextButton(
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
									]
								)
							),
							Container(
								margin=margin.only(top=(SPACING * 2)),
								content=Column(
									controls=[
										self.btn_submit,
										Divider(),
										self.btn_sign_up
									]
								)
							),
							Container(
								margin=margin.only(top=(SPACING * 2)),
								width=(APP_WIDTH - (SPACING * 4)),
								content=Markdown(
									value=(
										"Para conocer más acerca de nuestra "
										"Política de Privacidad da click "
										"[aquí](https://www.google.com)."
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

	def validate(self, event: ControlEvent) -> None:
		if self.txt_password.value\
				and match(pattern=RGX_EMAIL, string=self.txt_email.value):
			self.btn_submit.disabled = False
		else:
			self.btn_submit.disabled = True
		self.page.update()

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
