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

	def bnr_handle_dismiss(self, event: ControlEvent) -> None:
		self.bnr_error.content = Text(value="")
		self.page.close(self.bnr_error)

	def btn_submit_clicked(self, event: ControlEvent) -> None:
		logger.info("Verificando que el registro exista...")
		response: Response = post(
			url=f"{BACK_END_URL}/{AUTH_USER_ENDPOINT}",
			headers={"Content-Type": "application/json"},
			json={
				"email": self.txt_email.value,
				"password": self.txt_password.value
			}
		)

		if response.status_code == 200:
			token = response.json()["token"]
			self.basket.session_token = token
			go_to_view(page=self.page, logger=logger, route="home")
		elif response.status_code == 401:
			self.bnr_error.content = Text(
				value="Usuario y/o contraseña incorrectos.",
				style=TextStyle(color=colors.RED)
			)
			self.page.open(self.bnr_error)
		else:
			self.bnr_error.content = Text(
				value=(
					"Ocurrió un error al iniciar sesión. "
					"Favor de intentarlo de nuevo más tarde."
				),
				style=TextStyle(color=colors.RED)
			)
			self.page.open(self.bnr_error)
