from re import match
from logging import getLogger, info
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Banner, Text, TextField, ElevatedButton,
	Divider, padding, margin, icons, ControlEvent
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


class ChangePasswordView:
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

		self.txt_confirm_password: TextField = TextField(
			prefix_icon=icons.LOCK,
			hint_text="Contraseña",
			password=True,
			can_reveal_password=True,
			on_change=self.validate,
			**txt_style
		)

		self.btn_submit: ElevatedButton = ElevatedButton(
			text="Continuar",
			on_hover=main_btn_hover,
			on_click=self.btn_submit_clicked,
			**btn_primary_style
		)

		self.btn_back: ElevatedButton = ElevatedButton(
			icon=icons.LOGIN,
			text="Regresar a Iniciar sesión",
			on_hover=secondary_btn_hover,
			on_click=self.btn_back_clicked,
			**btn_secondary_style
		)

		self.cont_email: Container = Container(
			content=Column(
				controls=[
					Text(
						value=(
							"Ingresa tu correo electrónico "
							"para cambiar tu contraseña:"
						)
					),
					Container(content=self.txt_email)
				]
			)
		)

		self.cont_password: Container = Container(
			visible=False,
			content=Column(
				controls=[
					Text(value="Ingresa una contraseña nueva:"),
					Container(content=self.txt_password)
				]
			)
		)

		self.cont_confirm_password: Container = Container(
			visible=False,
			content=Column(
				controls=[
					Text(value="Confirmar contraseña nueva:"),
					Container(content=self.txt_confirm_password)
				]
			)
		)

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		return View(
			route="/change_password",
			padding=padding.all(value=0.0),
			bgcolor=MAIN_COLOR,
			controls=[
				Container(
					content=Column(
						controls=[
							MainTitleColumn(
								subtitle="Cambiar contraseña",
								top_margin=(SPACING * 2)
							),
							Divider(height=SPACING, color="white"),
							Column(
								spacing=SPACING,
								controls=[
									self.cont_email,
									self.cont_password,
									self.cont_confirm_password
								]
							),
							Container(
								margin=margin.only(top=(SPACING * 3)),
								content=Column(
									controls=[
										self.btn_submit,
										Divider(),
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
		# Case when only txt_email is displayed
		if not self.cont_password.visible and not self.cont_confirm_password.visible\
				and match(pattern=RGX_EMAIL, string=self.txt_email.value):
			self.btn_submit.disabled = False
		# Case when only txt_email and cont_password and cont_confirm_password are all displayed
		elif self.cont_password.visible and self.cont_confirm_password.visible\
			and all([
				self.txt_password.value,
				self.txt_confirm_password.value,
				match(pattern=RGX_EMAIL, string=self.txt_email.value)]):
			self.btn_submit.disabled = False
		else:
			self.btn_submit.disabled = True

		self.page.update()

	def btn_back_clicked(self, event: ControlEvent) -> None:
		self.cont_password.visible = False
		self.cont_confirm_password.visible = False
		self.page.update()

		go_to_view(page=self.page, logger=logger, route=""),  # '/'

	def btn_submit_clicked(self, event: ControlEvent) -> None:
		if self.cont_password.visible and self.cont_confirm_password.visible:
			info("Cambiando contraseña...")
		else:
			self.btn_submit.disabled = True
			self.cont_password.visible = True
			self.cont_confirm_password.visible = True
			self.page.update()
