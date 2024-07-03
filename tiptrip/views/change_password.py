from re import match
from logging import getLogger, info
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Banner, Text, TextField, ElevatedButton,
	IconButton, Divider, padding, margin, icons, ControlEvent
)

from resources.config import *
from resources.styles import *
from resources.functions import *
from components.titles import MainTitle
# from data import db
# from components.banners import ErrorBanner


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class ChangePasswordView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None
		self.btn_submit = None
		self.btn_back = None

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

		self.txt_confirm_password: TextField = TextField(
			prefix_icon=icons.LOCK,
			hint_text="Confirmar contraseña",
			password=True,
			can_reveal_password=True,
			**txt_style
		)

		self.cont_email: Container = Container(
			content=Column(
				controls=[
					Container(
						content=Text(
							value=(
								"Ingresa tu correo electrónico "
								"para cambiar tu contraseña:"
							),
							color=colors.BLACK
						)
					),
					Container(
						height=TXT_CONT_SIZE,
						content=self.txt_email,
					)
				]
			)
		)

		self.cont_password: Container = Container(
			visible=False,
			content=Column(
				controls=[
					Container(
						content=Text(
							value="Ingresa una contraseña nueva:",
							color=colors.BLACK
						)
					),
					Container(
						height=TXT_CONT_SIZE,
						content=self.txt_password,
					)
				]
			)
		)

		self.cont_confirm_password: Container = Container(
			visible=False,
			content=Column(
				controls=[
					Container(
						content=Text(
							value="Confirmar contraseña nueva:",
							color=colors.BLACK
						)
					),
					Container(
						height=TXT_CONT_SIZE,
						content=self.txt_confirm_password,
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
			text="Continuar",
			on_click=self.btn_submit_clicked,
			**btn_primary_style
		)

		self.btn_back: ElevatedButton = ElevatedButton(
			width=self.page.width,
			content=Text(value="Regresar a Iniciar sesión", size=BTN_TEXT_SIZE),
			on_click=self.btn_back_clicked,
			**btn_secondary_style
		)

		return View(
			route="/change_password",
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
								subtitle="Cambiar contraseña",
								top_margin=(SPACING * 2)
							),
							Container(
								margin=margin.only(top=SPACING),
								content=Column(
									spacing=(SPACING * 1.5),
									controls=[
										self.cont_email,
										self.cont_password,
										self.cont_confirm_password
									]
								)
							),
							Container(
								margin=margin.only(top=(SPACING * 4)),
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

	# def validate(self, event: ControlEvent) -> None:
	# 	# Case when only txt_email is displayed
	# 	if not self.cont_password.visible and not self.cont_confirm_password.visible\
	# 			and match(pattern=RGX_EMAIL, string=self.txt_email.value):
	# 		self.btn_submit.disabled = False
	# 	# Case when only txt_email and cont_password and cont_confirm_password are all displayed
	# 	elif self.cont_password.visible and self.cont_confirm_password.visible\
	# 		and all([
	# 			self.txt_password.value,
	# 			self.txt_confirm_password.value,
	# 			match(pattern=RGX_EMAIL, string=self.txt_email.value)]):
	# 		self.btn_submit.disabled = False
	# 	else:
	# 		self.btn_submit.disabled = True

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
			# self.btn_submit.disabled = True
			self.cont_password.visible = True
			self.cont_confirm_password.visible = True
			self.page.update()
