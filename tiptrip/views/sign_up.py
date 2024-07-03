from re import match
from logging import getLogger, info
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Row, Text, TextField,
	IconButton, ElevatedButton, Checkbox, Divider, MainAxisAlignment,
	CrossAxisAlignment, Markdown, padding, margin, icons, ControlEvent
)

# from data import db
from resources.config import *
from resources.styles import *
from resources.functions import *
from components.titles import MainTitle


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class SignUpView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.txt_username: TextField = TextField(
			prefix_icon=icons.ACCOUNT_CIRCLE,
			hint_text="Nombre de usuario",
			on_change=self.validate,
			**txt_style
		)

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

		self.txt_confirm_password: TextField = TextField(
			prefix_icon=icons.LOCK,
			hint_text="Confirmar contraseña",
			password=True,
			can_reveal_password=True,
			on_change=self.validate,
			**txt_style
		)

		self.chk_tyc: Checkbox = Checkbox(
			label="",
			value=False,
			active_color=SECONDARY_COLOR,
			on_change=self.validate
		)

		self.cont_tyc: Container = Container(
			# width=self.page.width,
			content=Row(
				alignment=MainAxisAlignment.START,
				vertical_alignment=CrossAxisAlignment.CENTER,
				spacing=0,
				controls=[
					self.chk_tyc,
					Markdown(
						value=(
							"Acepto [Términos y Condiciones]"
							"(https://www.google.com)."
						),
						on_tap_link=lambda _: go_to_view(
							page=self.page,
							logger=logger,
							route="terms_conditions"
						),
					)
				]
			)
		)

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.btn_submit: ElevatedButton = ElevatedButton(
			width=self.page.width,
			content=Text(
				value="Crear cuenta",
				size=BTN_TEXT_SIZE
			),
			on_click=self.btn_submit_clicked,
			**btn_primary_style
		)

		self.btn_back: ElevatedButton = ElevatedButton(
			width=self.page.width,
			content=Text(
				value="Regresar a Iniciar sesión",
				size=BTN_TEXT_SIZE
			),
			on_click=lambda _: go_to_view(
				page=self.page,
				logger=logger,
				route=""  # '/'
			),
			**btn_secondary_style
		)

		return View(
			route="/sign_up",
			padding=padding.all(value=0.0),
			bgcolor=MAIN_COLOR,
			controls=[
				Container(
					content=Column(
						controls=[
							Container(
								content=IconButton(
									icon=icons.ARROW_BACK,
									icon_color=colors.BLACK,
									on_click=lambda _: go_to_view(
										page=self.page,
										logger=logger,
										route=""  # '/'
									),
								)
							),
							MainTitle(
								subtitle="Registrarse",
								top_margin=(SPACING * 2)
							),
							Container(
								margin=margin.only(top=SPACING),
								content=Column(
									spacing=SPACING,
									controls=[
										Text(
											value=(
												"Ingresa los siguientes "
												"datos para crear tu nueva "
												"cuenta:"
											),
											color=colors.BLACK
										),
										Container(
											content=Column(
												spacing=SPACING,
												controls=[
													Container(
														height=TXT_CONT_SIZE,
														content=self.txt_username,
													),
													Container(
														height=TXT_CONT_SIZE,
														content=self.txt_email,
													),
													Container(
														height=TXT_CONT_SIZE,
														content=self.txt_password,
													),
													Container(
														height=TXT_CONT_SIZE,
														content=self.txt_confirm_password,
													),
													Container(
														content=self.cont_tyc
													)
												]
											)
										)
									]
								)
							),
							Container(
								margin=margin.only(top=SPACING),
								content=Column(
									controls=[
										self.btn_submit,
										Divider(color=colors.TRANSPARENT),
										self.btn_back
									]
								)
							)
						]
					),
					**cont_main_style
				)
			]
		)

	def validate(self, event: ControlEvent) -> None:
		if all([
			self.txt_username.value,
			match(pattern=RGX_EMAIL, string=self.txt_email.value),
			self.txt_password.value,
			self.txt_confirm_password.value,
			self.chk_tyc.value
		]):
			self.btn_submit.disabled = False
		else:
			self.btn_submit.disabled = True
		self.page.update()

	def btn_submit_clicked(self, event: ControlEvent) -> None:
		info("Creando cuenta...")
	# 	logger.info("Creando conexión a la base de datos...")
	# 	connection = db.connect_to_db()
	#
	# 	logger.info("Verificando que el registro exista...")
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
