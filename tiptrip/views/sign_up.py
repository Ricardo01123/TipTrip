import flet as ft
from re import match
from requests import post, Response
from logging import Logger, getLogger

from resources.config import *
from resources.styles import *
from resources.functions import *
from components.titles import MainTitle


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class SignUpView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page

		# Custom components
		self.txt_username: ft.TextField = ft.TextField(
			prefix_icon=ft.icons.ACCOUNT_CIRCLE,
			hint_text="Nombre de usuario",
			**txt_style
		)
		self.txt_email: ft.TextField = ft.TextField(
			prefix_icon=ft.icons.EMAIL,
			hint_text="Correo electrónico",
			**txt_style
		)
		self.txt_password: ft.TextField = ft.TextField(
			prefix_icon=ft.icons.LOCK,
			hint_text="Contraseña",
			password=True,
			can_reveal_password=True,
			on_change=self.validate,
			**txt_style
		)
		self.txt_confirm_password: ft.TextField = ft.TextField(
			prefix_icon=ft.icons.LOCK,
			hint_text="Confirmar contraseña",
			password=True,
			can_reveal_password=True,
			on_change=self.validate,
			**txt_style
		)
		self.chk_tyc: ft.Checkbox = ft.Checkbox(
			label="",
			value=False,
			active_color=SECONDARY_COLOR,
			on_change=self.validate
		)
		self.cont_tyc: ft.Container = ft.Container(
			content=ft.Row(
				alignment=ft.MainAxisAlignment.START,
				vertical_alignment=ft.CrossAxisAlignment.CENTER,
				spacing=0,
				controls=[
					self.chk_tyc,
					ft.Markdown(
						value=(
							"Acepto los [Términos y Condiciones]"
							"(https://www.google.com)."
						),
						md_style_sheet=ft.MarkdownStyleSheet(
							p_text_style=ft.TextStyle(color=ft.colors.BLACK)
						),
						on_tap_link=lambda _: go_to_view(page=self.page, logger=logger, route="/terms_conditions")
					)
				]
			)
		)
		self.lbl_username_required: ft.Text = ft.Text(
			value = "Campo requerido *",
			style=ft.TextStyle(color=ft.colors.RED),
			visible=False
		)
		self.lbl_email_required: ft.Text = ft.Text(
			value = "Campo requerido *",
			style=ft.TextStyle(color=ft.colors.RED),
			visible=False
		)
		self.lbl_password_required: ft.Text = ft.Text(
			value = "Campo requerido *",
			style=ft.TextStyle(color=ft.colors.RED),
			visible=False
		)
		self.lbl_confirm_password_required: ft.Text = ft.Text(
			value = "Campo requerido *",
			style=ft.TextStyle(color=ft.colors.RED),
			visible=False
		)
		self.lbl_pwd_match: ft.Text = ft.Text(
			value = "Las contraseñas no coinciden.",
			style=ft.TextStyle(color=ft.colors.RED),
			visible=False
		)
		self.lbl_tyc_required: ft.Text = ft.Text(
			value = "Los términos y condiciones deben ser aceptados para continuar.",
			style=ft.TextStyle(color=ft.colors.RED),
			visible=False
		)
		self.dlg_success: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Usuario creado"),
			content=ft.Text("El usuario ha sido creado correctamente."),
			actions=[
				ft.TextButton("Aceptar", on_click=self.dlg_handle_ok_button),
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=self.dlg_handle_ok_button
		)
		self.dlg_error: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text(""),
			content=ft.Text(""),
			actions=[
				ft.TextButton("Aceptar", on_click=lambda _: self.page.close(self.dlg_error)),
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_error)
		)
		self.btn_submit: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			content=ft.Text(
				value="Crear cuenta",
				size=BTN_TEXT_SIZE
			),
			on_click=self.btn_submit_clicked,
			**btn_primary_style
		)
		self.btn_back: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			content=ft.Text(
				value="Regresar a Iniciar sesión",
				size=BTN_TEXT_SIZE
			),
			on_click=self.handle_btn_back,
			**btn_secondary_style
		)

		# View native attributes
		super().__init__(
			route="/sign_up",
			bgcolor=MAIN_COLOR,
			padding=ft.padding.all(value=0.0),
			controls=[
				ft.Container(
					content=ft.Column(
						controls=[
							ft.Container(
								content=ft.IconButton(
									icon=ft.icons.ARROW_BACK,
									icon_color=ft.colors.BLACK,
									on_click=lambda _: go_to_view(page=self.page, logger=logger, route="/sign_in"),
								)
							),
							MainTitle(
								subtitle="Registrarse",
								top_margin=(SPACING / 2)
							),
							ft.Container(
								margin=ft.margin.only(top=(SPACING / 2)),
								content=ft.Column(
									controls=[
										ft.Text(
											value=(
												"Ingresa los siguientes "
												"datos para crear tu nueva "
												"cuenta:"
											),
											color=ft.colors.BLACK
										),
										ft.Container(
											content=ft.Column(
												controls=[
													ft.Container(
														height=TXT_CONT_SIZE,
														content=self.txt_username,
													),
													ft.Container(content=self.lbl_username_required),
													ft.Container(
														height=TXT_CONT_SIZE,
														content=self.txt_email,
													),
													ft.Container(content=self.lbl_email_required),
													ft.Container(
														height=TXT_CONT_SIZE,
														content=self.txt_password,
													),
													ft.Container(content=self.lbl_password_required),
													ft.Container(
														height=TXT_CONT_SIZE,
														content=self.txt_confirm_password,
													),
													ft.Container(content=self.lbl_confirm_password_required),
													ft.Container(content=self.lbl_pwd_match),
													ft.Container(content=self.cont_tyc),
													ft.Container(content=self.lbl_tyc_required)
												]
											)
										)
									]
								)
							),
							ft.Container(
								margin=ft.margin.only(top=(SPACING / 2)),
								content=ft.Column(
									controls=[
										self.btn_submit,
										# ft.Divider(color=ft.colors.TRANSPARENT),
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

	def validate(self, _: ft.ControlEvent) -> None:
		if self.txt_password.value != "" or self.txt_confirm_password.value != "":
			if self.txt_password.value:
				self.lbl_password_required.visible = False

			if self.txt_confirm_password.value:
				self.lbl_confirm_password_required.visible = False

			if self.txt_password.value != self.txt_confirm_password.value:
				self.lbl_pwd_match.visible = True
			else:
				self.lbl_pwd_match.visible = False

		else:
			self.lbl_pwd_match.visible = False

		self.page.update()

	def dlg_handle_ok_button(self, _: ft.ControlEvent) -> None:
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

		if response.status_code == 201:
			logger.info("User authenticated successfully")

			logger.info("Adding user data to session data...")
			data: dict = response.json()
			self.page.session.set(key="aux", value=None) # This is a workaround to avoid a bug in the framework
			self.page.session.set(key="id", value=data["id"])
			self.page.session.set(key="email", value=self.txt_email.value)
			self.page.session.set(key="username", value=data["username"])
			self.page.session.set(key="session_token", value=data["token"])
			self.page.session.set(key="created_at", value=data["created_at"])
			self.page.session.set(key="places_data", value=None)

			logger.info("Cleaning text fields...")
			self.txt_username.value = ""
			self.txt_email.value = ""
			self.txt_password.value = ""
			self.txt_confirm_password.value = ""
			self.chk_tyc.value = False

			self.page.update()

			go_to_view(page=self.page, logger=logger, route="/permissions")

		else:
			logger.error("An error occurred while trying to authenticate user")
			self.dlg_error.title = ft.Text(value="Error al iniciar sesión")
			self.dlg_error.content = ft.Text(
				value=(
					"Ocurrió un error al iniciar sesión. "
					"Favor de intentarlo de nuevo más tarde."
				)
			)
			self.page.open(self.dlg_error)

	def handle_btn_back(self, _: ft.ControlEvent) -> None:
		logger.info("Cleaning text fields...")
		self.txt_username.value = ""
		self.txt_email.value = ""
		self.txt_password.value = ""
		self.txt_confirm_password.value = ""

		logger.info("Cleaning required messages...")
		self.lbl_username_required.visible = False
		self.lbl_email_required.visible = False
		self.lbl_password_required.visible = False
		self.lbl_confirm_password_required.visible = False
		self.lbl_pwd_match.visible = False
		self.lbl_tyc_required.visible = False

		go_to_view(page=self.page, logger=logger, route="/sign_in")

	def btn_submit_clicked(self, _: ft.ControlEvent) -> None:
		username_txt_filled: bool = False
		email_txt_filled: bool = False
		password_txt_filled: bool = False
		confirm_password_txt_filled: bool = False

		logger.info("Checking if sign up fields are filled...")
		if not self.txt_username.value:
			self.lbl_username_required.visible = True
			username_txt_filled = False
		else:
			self.lbl_username_required.visible = False
			username_txt_filled = True

		if not self.txt_email.value:
			self.lbl_email_required.visible = True
			email_txt_filled = False
		else:
			self.lbl_email_required.visible = False
			email_txt_filled = True

		if not self.txt_password.value:
			self.lbl_password_required.visible = True
			password_txt_filled = False
		else:
			self.lbl_password_required.visible = False
			password_txt_filled = True

		if not self.txt_confirm_password.value:
			self.lbl_confirm_password_required.visible = True
			confirm_password_txt_filled = False
		else:
			self.lbl_confirm_password_required.visible = False
			confirm_password_txt_filled = True

		if not self.chk_tyc.value:
			self.lbl_tyc_required.visible = True
		else:
			self.lbl_tyc_required.visible = False

		self.page.update()

		if all([
			username_txt_filled,
			email_txt_filled,
			password_txt_filled,
			confirm_password_txt_filled,
			self.chk_tyc.value
		]):
			if self.lbl_pwd_match.visible:
				logger.info("Passwords do not match. Aborting process...")
				self.dlg_error.title = ft.Text(value="Las contraseñas no coinciden")
				self.dlg_error.content = ft.Text(value="Las contraseñas no coinciden. Favor de verificarlas.")
				self.page.open(self.dlg_error)

			elif not match(pattern=RGX_EMAIL, string=self.txt_email.value):
				logger.info("Invalid email format. Aborting process...")
				self.dlg_error.title = ft.Text(value="Formato de correo inválido")
				self.dlg_error.content = ft.Text(value="El correo electrónico ingresado no es válido. Favor de verificarlo.")
				self.page.open(self.dlg_error)

			else:
				logger.info("Creating new user...")
				response: Response = post(
					url=f"{BACK_END_URL}/{USERS_ENDPOINT}",
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
					self.dlg_error.title = ft.Text(value="Error al crear usuario")
					self.dlg_error.content = ft.Text(
						value=(
							"El correo electrónico proporcionado ya fue usado.\n"
							"Favor de usar uno diferente."
						),
					)
					self.page.open(self.dlg_error)

				else:
					logger.error("Error creating user")
					self.dlg_error.title = ft.Text(value="Error al crear usuario")
					self.dlg_error.content = ft.Text(
						value=(
							"Ocurrió un error al crear el usuario. "
							"Favor de intentarlo de nuevo más tarde."
						)
					)
					self.page.open(self.dlg_error)
