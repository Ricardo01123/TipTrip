import logging
from re import match
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Banner, Text, TextField, ElevatedButton, Icon, Divider,
	alignment, padding, margin, BoxShadow, border_radius, colors, icons, ControlEvent
)

from data import db
from resources.config import *
from components.banners import ErrorBanner
from resources.functions import main_btn_hover, secondary_btn_hover, go_to_view, load_user_to_basket


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


class ChangePasswordView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

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
			label="Contraseña",
			cursor_color=SECONDARY_COLOR,
			focused_border_color=SECONDARY_COLOR,
			password=True,
			can_reveal_password=True,
			on_change=self.validate
		)

		self.btn_submit: ElevatedButton = ElevatedButton(
			text="Continuar",
			color=colors.WHITE,
			bgcolor=MAIN_COLOR,
			width=(TOTAL_WIDTH - (MARGIN * 4)),
			disabled=True,
			on_hover=main_btn_hover,
			on_click=self.btn_submit_clicked
		)

		self.btn_back: ElevatedButton = ElevatedButton(
			icon=icons.LOGIN,
			text="Regresar a Iniciar sesión",
			color=MAIN_COLOR,
			width=(TOTAL_WIDTH - (MARGIN * 4)),
			on_hover=secondary_btn_hover,
			on_click=self.btn_back_clicked
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
										content=Text(value="Cambiar contraseña", size=TEXT_SIZE)
									)
								]
							),
							Container(
								margin=margin.only(top=(MARGIN * 3)),
								content=Column(
									controls=[
										Text(
											value=(
												"Ingresa tu correo electrónico de inicio de sesión para "
												"cambiar tu contraseña:"
											)
										),
										Container(
											margin=margin.only(top=(MARGIN * 2)),
											content=self.txt_email
										),
										self.cont_password,
										self.cont_confirm_password
									]
								)
							),
							Container(
								margin=margin.only(top=(MARGIN * 2)),
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
			print("Cambiando contraseña...")
		else:
			self.btn_submit.disabled = True
			self.cont_password.visible = True
			self.cont_confirm_password.visible = True
			self.page.update()
