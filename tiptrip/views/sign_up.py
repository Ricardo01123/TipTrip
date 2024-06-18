import logging
from re import match
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Row, Banner, Text, TextField, ElevatedButton, Checkbox, Icon, Divider,
	CrossAxisAlignment, alignment, Markdown, padding, margin, BoxShadow, border_radius, colors, icons, ControlEvent
)

from data import db
from resources.config import *
from components.banners import ErrorBanner
from resources.functions import main_btn_hover, secondary_btn_hover, go_to_view, load_user_to_basket


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


class SignUpView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.txt_username: TextField = TextField(
			prefix_icon=icons.SUPERVISED_USER_CIRCLE_OUTLINED,
			label="Nombre de usuario",
			cursor_color=SECONDARY_COLOR,
			focused_border_color=SECONDARY_COLOR,
			on_change=self.validate
		)

		self.txt_email: TextField = TextField(
			prefix_icon=icons.EMAIL,
			label="Correo electrónico",
			cursor_color=SECONDARY_COLOR,
			focused_border_color=SECONDARY_COLOR,
			on_change=self.validate
		)

		self.txt_password: TextField = TextField(
			prefix_icon=icons.LOCK,
			label="Contraseña",
			cursor_color=SECONDARY_COLOR,
			focused_border_color=SECONDARY_COLOR,
			password=True,
			can_reveal_password=True,
			on_change=self.validate
		)

		self.txt_confirm_password: TextField = TextField(
			prefix_icon=icons.LOCK,
			label="Confirmar contraseña",
			cursor_color=SECONDARY_COLOR,
			focused_border_color=SECONDARY_COLOR,
			password=True,
			can_reveal_password=True,
			on_change=self.validate
		)

		self.chk_tyc: Checkbox = Checkbox(
			label="",
			value=False,
			active_color=SECONDARY_COLOR,
			on_change=self.validate
		)

		self.cont_tyc: Container = Container(
			content=Row(
				vertical_alignment=CrossAxisAlignment.CENTER,
				controls=[
					self.chk_tyc,
					Markdown(
						value="Acepto [Términos y Condiciones](https://www.google.com).",
						on_tap_link=lambda _: go_to_view(page=self.page, logger=logger, route="terms_conditions"),
					)
				]
			)
		)

		self.btn_submit: ElevatedButton = ElevatedButton(
			text="Crear cuenta",
			color=colors.WHITE,
			bgcolor=MAIN_COLOR,
			width=(TOTAL_WIDTH - (MARGIN * 4)),
			disabled=True,
			on_hover=main_btn_hover
			# on_click=self.btn_submit_clicked
		)

		self.btn_back: ElevatedButton = ElevatedButton(
			icon=icons.LOGIN,
			text="Regresar a iniciar sesión",
			color=MAIN_COLOR,
			width=(TOTAL_WIDTH - (MARGIN * 4)),
			on_hover=secondary_btn_hover,
			on_click=lambda _: go_to_view(page=self.page, logger=logger, route=""),  # '/'
		)

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.page.banner = ErrorBanner(page)

		return View(
			route="/sign_up",
			padding=padding.all(value=0.0),
			bgcolor=MAIN_COLOR,
			controls=[
				Container(
					width=TOTAL_WIDTH,
					height=(HEIGHT_WITHOUT_HEADER - (MARGIN * 2)),
					margin=margin.all(value=MARGIN),
					padding=padding.all(value=PADDING),
					border_radius=border_radius.all(value=RADIUS),
					bgcolor=colors.WHITE,
					shadow=BoxShadow(blur_radius=BLUR),
					content=Column(
						controls=[
							Column(
								controls=[
									Container(
										margin=margin.only(top=(MARGIN * 2)),
										alignment=alignment.center,
										content=Text(value=PROJECT_NAME, size=TITLE_SIZE),
									),
									Container(
										alignment=alignment.center,
										content=Text(value="Registrarse", size=TEXT_SIZE)
									)
								]
							),
							Container(
								margin=margin.only(top=MARGIN),
								content=Column(
									controls=[
										Text(value="Ingresa los siguientes datos para crear tu nueva cuenta:"),
										Container(
											margin=margin.only(top=(MARGIN * 2)),
											content=Column(
												controls=[
													self.txt_username,
													self.txt_email,
													self.txt_password,
													self.txt_confirm_password,
													self.cont_tyc
												]
											)
										)
									]
								)
							),
							Container(
								margin=margin.only(top=MARGIN),
								content=Column(
									controls=[
										self.btn_submit,
										Divider(),
										self.btn_back
									]
								)
							)
						]
					)
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
	#
	# def btn_submit_clicked(self, event: ControlEvent) -> None:
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
