import flet as ft
from re import match
from logging import Logger, getLogger

from requests import post, Response
from requests.exceptions import ConnectTimeout

from resources.config import *
from resources.styles import *
from resources.functions import *
from components.splash import Splash
from components.titles import MainTitle


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class SignUpView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page

		# Custom components
		self.txt_username: ft.TextField = ft.TextField(
			prefix_icon=ft.Icons.ACCOUNT_CIRCLE,
			label="Nombre de usuario",
			hint_text="Fernanda",
			autofocus=True,
			**txt_style
		)
		self.txt_email: ft.TextField = ft.TextField(
			prefix_icon=ft.Icons.EMAIL,
			label="Correo electrónico",
			hint_text="ejemplo@ejemplo.com",
			**txt_style
		)
		self.txt_password: ft.TextField = ft.TextField(
			prefix_icon=ft.Icons.LOCK,
			label="Contraseña",
			password=True,
			can_reveal_password=True,
			on_change=self.validate,
			**txt_style
		)
		self.txt_confirm_password: ft.TextField = ft.TextField(
			prefix_icon=ft.Icons.LOCK,
			label="Confirmar contraseña",
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
			content=ft.ResponsiveRow(
				alignment=ft.MainAxisAlignment.START,
				vertical_alignment=ft.CrossAxisAlignment.CENTER,
				spacing=0,
				controls=[
					ft.Column(
						col=2,
						controls=[self.chk_tyc]
					),
					ft.Column(
						col=10,
						controls=[
							ft.Markdown(
								value=(
									"Acepto los [Términos y Condiciones]"
									"(https://www.google.com)."
								),
								md_style_sheet=ft.MarkdownStyleSheet(
									p_text_style=ft.TextStyle(color=ft.Colors.BLACK)
								),
								on_tap_link=lambda _: go_to_view(page=self.page, logger=logger, route="/terms_conditions")
							)
						]
					)
				]
			)
		)
		self.lbl_username_required: ft.Text = ft.Text(
			value = "Campo requerido *",
			style=ft.TextStyle(color=ft.Colors.RED),
			visible=False
		)
		self.lbl_email_required: ft.Text = ft.Text(
			value = "Campo requerido *",
			style=ft.TextStyle(color=ft.Colors.RED),
			visible=False
		)
		self.lbl_password_required: ft.Text = ft.Text(
			value = "Campo requerido *",
			style=ft.TextStyle(color=ft.Colors.RED),
			visible=False
		)
		self.lbl_confirm_password_required: ft.Text = ft.Text(
			value = "Campo requerido *",
			style=ft.TextStyle(color=ft.Colors.RED),
			visible=False
		)
		self.lbl_pwd_match: ft.Text = ft.Text(
			value = "Las contraseñas no coinciden.",
			style=ft.TextStyle(color=ft.Colors.RED),
			visible=False
		)
		self.lbl_tyc_required: ft.Text = ft.Text(
			value = "Los términos y condiciones deben ser aceptados para continuar.",
			style=ft.TextStyle(color=ft.Colors.RED),
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

		# Splash components
		self.splash = Splash(page=self.page)
		self.page.overlay.append(self.splash)
		self.cont_splash = ft.Container(
			expand=True,
			width=self.page.width,
			bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
			content=None,
			visible=False
		)

		# View native attributes
		super().__init__(
			route="/sign_up",
			bgcolor=MAIN_COLOR,
			padding=ft.padding.all(value=0.0),
			controls=[
				ft.Container(
					expand=True,
					content=ft.Stack(
						controls=[
							ft.Container(
								height=self.page.height,
								content=ft.Column(
									scroll=ft.ScrollMode.HIDDEN,
									controls=[
										ft.Container(
											content=ft.IconButton(
												icon=ft.Icons.ARROW_BACK,
												icon_color=ft.Colors.BLACK,
												on_click=lambda _: go_to_view(page=self.page, logger=logger, route="/sign_in"),
											)
										),
										MainTitle(
											subtitle="Registrarse",
											top_margin=10
										),
										ft.Container(
											margin=ft.margin.only(top=SPACING),
											content=ft.Column(
												controls=[
													ft.Text(
														value=(
															"Ingresa los siguientes "
															"datos para crear tu nueva "
															"cuenta:"
														),
														color=ft.Colors.BLACK
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
											margin=ft.margin.symmetric(vertical=SPACING),
											content=ft.Column(
												controls=[
													self.btn_submit,
													self.btn_back
												]
											)
										)
									]
								),
								**cont_main_style
							),
							self.cont_splash
						]
					)
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

		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()

	def dlg_handle_ok_button(self, _: ft.ControlEvent) -> None:
		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()

		try:
			self.page.close(self.dlg_success)
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.close(self.dlg_success)

		logger.info("Showing loading splash screen...")
		self.cont_splash.visible = True
		self.splash.visible = True
		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()

		logger.info("Authenticating user...")

		try:
			response: Response = post(
				url=f"{BACK_END_URL}/{AUTH_USER_ENDPOINT}",
				headers={"Content-Type": "application/json"},
				json={
					"mail": self.txt_email.value.strip(),
					"password": self.txt_password.value.strip()
				}
			)

		except ConnectTimeout:
			logger.error("Connection timeout while authenticating user")
			self.dlg_error.title = ft.Text(value="Error de conexión a internet")
			self.dlg_error.content = ft.Text(
				value=(
					"Ocurrió un error al intentar autenticar al usuario. "
					"Favor de intentarlo de nuevo más tarde."
				)
			)

			logger.info("Hidding loading splash screen...")
			self.cont_splash.visible = False
			self.splash.visible = False
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()

			try:
				self.page.open(self.dlg_error)
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.open(self.dlg_error)
			finally:
				return

		if response.status_code == 201:
			logger.info("User authenticated successfully")

			data: dict = response.json()
			logger.info("Setting session data...")
			# User variables
			self.page.session.set(key="aux", value=None) # This is a workaround to avoid a bug in the framework
			self.page.session.set(key="id", value=data["id"])
			self.page.session.set(key="email", value=self.txt_email.value)
			self.page.session.set(key="username", value=data["username"])
			self.page.session.set(key="session_token", value=data["token"])
			self.page.session.set(key="created_at", value=data["created_at"])
			# Home variables
			self.page.session.set(key="places_data", value=None)
			self.page.session.set(key="drd_classification_value", value="")
			self.page.session.set(key="drd_municipality_value", value="")
			self.page.session.set(key="sld_value", value=7)
			# Map variables
			self.page.session.set(key="map_places_data", value=None)
			self.page.session.set(key="map_sld_value", value=7)
			self.page.session.set(key="map_drd_value", value="")

			logger.info("Cleaning text fields...")
			self.txt_username.value = ""
			self.txt_email.value = ""
			self.txt_password.value = ""
			self.txt_confirm_password.value = ""
			self.chk_tyc.value = False

			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)
				self.page.update()

			logger.info("Hidding loading splash screen...")
			self.cont_splash.visible = False
			self.splash.visible = False
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)
				self.page.update()

			try:
				go_to_view(page=self.page, logger=logger, route="/permissions")
			except Exception as e:
				logger.error(f"Error: {e}")
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)
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

			logger.info("Hidding loading splash screen...")
			self.cont_splash.visible = False
			self.splash.visible = False
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)
				self.page.update()

			try:
				self.page.open(self.dlg_error)
			except Exception as e:
				logger.error(f"Error: {e}")
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)
				self.page.open(self.dlg_error)
			finally:
				return

	def handle_btn_back(self, _: ft.ControlEvent) -> None:
		logger.info("Showing loading splash screen...")
		self.cont_splash.visible = True
		self.splash.visible = True
		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()

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

		logger.info("Hidding loading splash screen...")
		self.cont_splash.visible = False
		self.splash.visible = False
		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()

		try:
			go_to_view(page=self.page, logger=logger, route="/sign_in")
		except Exception as e:
			logger.error(f"Error: {e}")
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

		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()

		if all([
			username_txt_filled,
			email_txt_filled,
			password_txt_filled,
			confirm_password_txt_filled,
			self.chk_tyc.value
		]):
			if self.lbl_pwd_match.visible:
				logger.warning("Passwords do not match. Aborting process...")
				self.dlg_error.title = ft.Text(value="Las contraseñas no coinciden")
				self.dlg_error.content = ft.Text(value="Las contraseñas no coinciden. Favor de verificarlas.")
				self.page.open(self.dlg_error)

			elif not match(pattern=RGX_EMAIL, string=self.txt_email.value):
				logger.warning("Invalid email format. Aborting process...")
				self.dlg_error.title = ft.Text(value="Formato de correo inválido")
				self.dlg_error.content = ft.Text(value="El correo electrónico ingresado no es válido. Favor de verificarlo.")
				self.page.open(self.dlg_error)

			else:
				logger.info("Showing loading splash screen...")
				self.cont_splash.visible = True
				self.splash.visible = True
				try:
					self.page.update()
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.update()

				logger.info("Creating new user...")
				try:
					response: Response = post(
						url=f"{BACK_END_URL}/{USERS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"username": self.txt_username.value.strip(),
							"mail": self.txt_email.value.strip(),
							"password": self.txt_password.value.strip(),
						}
					)

				except ConnectTimeout:
					logger.error("Connection timeout while creating user")
					self.dlg_error.title = ft.Text(value="Error de conexión a internet")
					self.dlg_error.content = ft.Text(
						value=(
							"No se pudo crear el usuario. "
							"Favor de revisar su conexión a internet e intentarlo de nuevo más tarde."
						)
					)

					logger.info("Hidding loading splash screen...")
					self.cont_splash.visible = False
					self.splash.visible = False
					try:
						self.page.update()
					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.update()

					try:
						self.page.open(self.dlg_error)
					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.open(self.dlg_error)
					finally:
						return

				if response.status_code == 201:
					logger.info("New user created successfully")

					logger.info("Hidding loading splash screen...")
					self.cont_splash.visible = False
					self.splash.visible = False
					try:
						self.page.update()
					except Exception as e:
						logger.error(f"Error: {e}")
						#! COMMENT
						post(
							url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
							headers={"Content-Type": "application/json"},
							json={
								"user_id": response.json()["id"],
								"file": encode_logfile()
							}
						)
						self.page.update()

					try:
						self.page.open(self.dlg_success)
					except Exception as e:
						logger.error(f"Error: {e}")
						#! COMMENT
						post(
							url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
							headers={"Content-Type": "application/json"},
							json={
								"user_id": response.json()["id"],
								"file": encode_logfile()
							}
						)
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

					logger.info("Hidding loading splash screen...")
					self.cont_splash.visible = False
					self.splash.visible = False
					self.page.update()

					try:
						self.page.update()
					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.update()

					try:
						self.page.open(self.dlg_error)
					except Exception as e:
						logger.error(f"Error: {e}")
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

					logger.info("Hidding loading splash screen...")
					self.cont_splash.visible = False
					self.splash.visible = False
					try:
						self.page.update()
					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.update()

					try:
						self.page.open(self.dlg_error)
					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.open(self.dlg_error)
