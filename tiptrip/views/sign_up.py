from re import match
from logging import getLogger
from requests import post, Response
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Row, Text, TextField, AlertDialog, Banner,
	IconButton, ElevatedButton, TextButton, Checkbox, Divider, Markdown, Icon,
	MainAxisAlignment, CrossAxisAlignment, padding, margin, icons, ControlEvent,
	ButtonStyle, TextStyle
)

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

		self.lbl_pwd_match: Text = Text(
			value = "Las contraseñas no coinciden.",
			style=TextStyle(color=colors.RED),
			visible=False
		)

		self.chk_tyc: Checkbox = Checkbox(
			label="",
			value=False,
			active_color=SECONDARY_COLOR,
			on_change=self.validate
		)

		self.cont_tyc: Container = Container(
			content=Row(
				alignment=MainAxisAlignment.START,
				vertical_alignment=CrossAxisAlignment.CENTER,
				spacing=0,
				controls=[
					self.chk_tyc,
					Markdown(
						value=(
							"Acepto los [Términos y Condiciones]"
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

		self.dlg_success: AlertDialog = AlertDialog(
			modal=True,
			title=Text("Usuario creado"),
			content=Text("El usuario ha sido creado correctamente."),
			actions=[
				TextButton("Aceptar", on_click=self.dlg_handle_dismiss),
			],
			actions_alignment=MainAxisAlignment.END,
			on_dismiss=self.dlg_handle_dismiss
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
			disabled=True,
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
								top_margin=SPACING
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
														content=self.lbl_pwd_match
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
		if self.txt_password.value != self.txt_confirm_password.value:
			self.lbl_pwd_match.visible = True
			self.page.update()
		else:
			self.lbl_pwd_match.visible = False
			self.page.update()

		if self.lbl_pwd_match.visible == False and all([
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

	def dlg_handle_dismiss(self, event: ControlEvent) -> None:
		self.page.close(self.dlg_success)
		go_to_view(
				page=self.page,
				logger=logger,
				route=""  # '/'
			),

	def bnr_handle_dismiss(self, event: ControlEvent) -> None:
		self.bnr_error.content = Text(value="")
		self.page.close(self.bnr_error)

	def btn_submit_clicked(self, event: ControlEvent) -> None:
		logger.info("Creando cuenta...")
		response: Response = post(
			url=f"{BACK_END_URL}/{ADD_USER_ENDPOINT}",
			headers={"Content-Type": "application/json"},
			json={
				"username": self.txt_username.value,
				"email": self.txt_email.value,
				"password": self.txt_password.value,
				"role": None,
				"image_path": None,
			}
		)

		if response.status_code == 201:
			self.page.open(self.dlg_success)
		elif response.status_code == 409:
			self.bnr_error.content = Text(
				value="El correo electrónico proporcionado ya fue usado.",
				style=TextStyle(color=colors.RED)
			)
			self.page.open(self.bnr_error)
		else:
			self.bnr_error.content = Text(
				value=(
					"Ocurrió un error al crear el usuario. "
					"Favor de intentarlo de nuevo más tarde."
				),
				style=TextStyle(color=colors.RED)
			)
			self.page.open(self.bnr_error)
