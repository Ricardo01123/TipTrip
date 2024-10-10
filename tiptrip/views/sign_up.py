from flet import *
from re import match
from logging import getLogger
from requests import post, Response
from flet_route import Params, Basket

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
				TextButton("Aceptar", on_click=self.dlg_handle_ok_button),
			],
			actions_alignment=MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_geolocator_info)
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

	def validate(self, _: ControlEvent) -> None:
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

	def dlg_handle_ok_button(self, _: ControlEvent) -> None:
		self.page.close(self.dlg_success)
		logger.info("Authenticating user...")

		response: Response = post(
			url=f"{BACK_END_URL}/{AUTH_USER_ENDPOINT}",
			headers={"Content-Type": "application/json"},
			json={
				"mail": self.txt_email.value,
				"password": self.txt_password.value
			}
		)

		if response.status_code == 200:
			logger.info("User authenticated successfully")

			logger.info("Adding user data to session data...")
			data = response.json()
			self.basket.email = self.txt_email.value
			self.basket.username = data["username"]
			self.basket.session_token = data["token"]
			self.basket.created_at = data["created_at"]

			logger.info("Cleaning text fields...")
			self.txt_username.value = ""
			self.txt_email.value = ""
			self.txt_password.value = ""
			self.txt_confirm_password.value = ""
			self.chk_tyc.value = False

			go_to_view(page=self.page, logger=logger, route="home")

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

	def dlg_handle_dismiss(self, _: ControlEvent) -> None:
		self.page.close(self.dlg_success)

	def bnr_handle_dismiss(self, _: ControlEvent) -> None:
		self.bnr_error.content = Text(value="")
		self.page.close(self.bnr_error)

	def btn_submit_clicked(self, _: ControlEvent) -> None:
		logger.info("Creating new user...")
		response: Response = post(
			url=f"{BACK_END_URL}/{ADD_USER_ENDPOINT}",
			headers={"Content-Type": "application/json"},
			json={
				"username": self.txt_username.value,
				"mail": self.txt_email.value,
				"password": self.txt_password.value,
			}
		)

		if response.status_code == 201:
			logger.info("New user created successfully")
			self.page.open(self.dlg_success)

		elif response.status_code == 409:
			logger.error("Email already exists")
			self.bnr_error.content = Text(
				value=(
					"El correo electrónico proporcionado ya fue usado.\n"
					"Favor de usar uno diferente."
				),
				style=TextStyle(color=colors.RED)
			)
			self.page.open(self.bnr_error)

		else:
			logger.error("Error creating user")
			self.bnr_error.content = Text(
				value=(
					"Ocurrió un error al crear el usuario. "
					"Favor de intentarlo de nuevo más tarde."
				),
				style=TextStyle(color=colors.RED)
			)
			self.page.open(self.bnr_error)
