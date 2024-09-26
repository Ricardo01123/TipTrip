from re import match
from logging import getLogger
from requests import post, Response
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Text, TextField, TextButton, ElevatedButton,
	Divider, Markdown, padding, margin, colors, icons, TextStyle, ScrollMode,
	ControlEvent, Banner, ButtonStyle, Icon
)

from resources.config import *
from resources.styles import *
from resources.functions import *
from components.titles import MainTitle


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
			on_change=self.validate,
			**txt_style
		)

		self.txt_password: TextField = TextField(
			prefix_icon=icons.LOCK,
			hint_text="Contraseña",
			on_change=self.validate,
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
			disabled=True,
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

		self.bnr_error: Banner = Banner(
			bgcolor=colors.RED_50,
			leading=Icon(
				icons.ERROR_OUTLINE_ROUNDED,
				color=colors.RED,
				size=40
			),
			content=Text(value=""),
			actions=[
				TextButton(
					text="Aceptar",
					style=ButtonStyle(color=colors.BLUE),
					on_click=self.bnr_handle_dismiss
				)
			],
			force_actions_below=True
		)

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

	def validate(self, _: ControlEvent) -> None:
		if match(pattern=RGX_EMAIL, string=self.txt_email.value) and self.txt_password.value:
			self.btn_submit.disabled = False
		else:
			self.btn_submit.disabled = True
		self.page.update()

	def bnr_handle_dismiss(self, _: ControlEvent) -> None:
		self.bnr_error.content = Text(value="")
		self.page.close(self.bnr_error)

	def btn_submit_clicked(self, _: ControlEvent) -> None:
		logger.info("Checking if credentials exists in DB...")
		response: Response = post(
			url=f"{BACK_END_URL}/{AUTH_USER_ENDPOINT}",
			headers={"Content-Type": "application/json"},
			json={
				"mail": self.txt_email.value,
				"pwd": self.txt_password.value
			}
		)

		if response.status_code == 200:
			data: dict = response.json()
			logger.info("User authenticated successfully")

			logger.info("Adding user data to session data...")
			self.basket.email = self.txt_email.value
			self.basket.username = data["username"]
			self.basket.session_token = data["token"]
			self.basket.created_at = data["created_at"]

			logger.info("Cleaning text fields...")
			self.txt_email.value = ""
			self.txt_password.value = ""

			go_to_view(page=self.page, logger=logger, route="home")

		elif response.status_code == 401:
			logger.info("User and/or password are incorrect")
			self.bnr_error.content = Text(
				value="Usuario y/o contraseña incorrectos.",
				style=TextStyle(color=colors.RED)
			)
			self.page.open(self.bnr_error)
		else:
			logger.error("An error occurred while trying to authenticate user")
			self.bnr_error.content = Text(
				value=(
					"Ocurrió un error al iniciar sesión. "
					"Favor de intentarlo de nuevo más tarde."
				),
				style=TextStyle(color=colors.RED)
			)
			self.page.open(self.bnr_error)
