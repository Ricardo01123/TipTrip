from flet import *
from re import match
from logging import getLogger
from requests import post, Response
from flet_route import Params, Basket

from resources.config import *
from resources.styles import *
from resources.functions import *
from components.titles import MainTitle
# from components.loading_ring import loading_ring


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class SignUpView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.txt_username: TextField = TextField(
			prefix_icon=icons.ACCOUNT_CIRCLE,
			hint_text="Nombre de usuario",
			**txt_style
		)

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
						md_style_sheet=MarkdownStyleSheet(
							p_text_style=TextStyle(color=colors.BLACK)
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

		self.lbl_username_required: Text = Text(
			value = "Campo requerido *",
			style=TextStyle(color=colors.RED),
			visible=False
		)

		self.lbl_email_required: Text = Text(
			value = "Campo requerido *",
			style=TextStyle(color=colors.RED),
			visible=False
		)

		self.lbl_password_required: Text = Text(
			value = "Campo requerido *",
			style=TextStyle(color=colors.RED),
			visible=False
		)

		self.lbl_confirm_password_required: Text = Text(
			value = "Campo requerido *",
			style=TextStyle(color=colors.RED),
			visible=False
		)

		self.lbl_pwd_match: Text = Text(
			value = "Las contraseñas no coinciden.",
			style=TextStyle(color=colors.RED),
			visible=False
		)

		self.lbl_tyc_required: Text = Text(
			value = "Los términos y condiciones deben ser aceptados para continuar.",
			style=TextStyle(color=colors.RED),
			visible=False
		)

		self.dlg_success: AlertDialog = AlertDialog(
			modal=True,
			title=Text("Usuario creado"),
			content=Text("El usuario ha sido creado correctamente."),
			actions=[
				TextButton("Aceptar", on_click=self.dlg_handle_ok_button),
			],
			actions_alignment=MainAxisAlignment.END,
			on_dismiss=self.dlg_handle_ok_button
		)

		self.dlg_error: AlertDialog = AlertDialog(
			modal=True,
			title=Text(""),
			content=Text(""),
			actions=[
				TextButton("Aceptar", on_click=lambda _: self.page.close(self.dlg_error)),
			],
			actions_alignment=MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_error)
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
			on_click=self.btn_submit_clicked,
			**btn_primary_style
		)

		self.btn_back: ElevatedButton = ElevatedButton(
			width=self.page.width,
			content=Text(
				value="Regresar a Iniciar sesión",
				size=BTN_TEXT_SIZE
			),
			on_click=self.handle_btn_back,
			**btn_secondary_style
		)

		# self.loading_ring: ProgressRing = ProgressRing(
		# 	visible=False,
		# 	stroke_align=-1,
		# 	width=LOADING_RING_SIZE,
		# 	height=LOADING_RING_SIZE,
		# 	stroke_width=5,
		# 	tooltip="Cargando...",
		# 	color=SECONDARY_COLOR,
		# 	left=(self.page.window.width // 2) - (LOADING_RING_SIZE // 2),
		# 	top = (self.page.window.height // 2) - (LOADING_RING_SIZE // 2)
		# )
		# self.page.overlay.append(self.loading_ring)

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
								top_margin=(SPACING / 2)
							),
							Container(
								margin=margin.only(top=(SPACING / 2)),
								content=Column(
									# spacing=(SPACING),
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
												# spacing=SPACING,
												controls=[
													Container(
														height=TXT_CONT_SIZE,
														content=self.txt_username,
													),
													Container(content=self.lbl_username_required),
													Container(
														height=TXT_CONT_SIZE,
														content=self.txt_email,
													),
													Container(content=self.lbl_email_required),
													Container(
														height=TXT_CONT_SIZE,
														content=self.txt_password,
													),
													Container(content=self.lbl_password_required),
													Container(
														height=TXT_CONT_SIZE,
														content=self.txt_confirm_password,
													),
													Container(content=self.lbl_confirm_password_required),
													Container(content=self.lbl_pwd_match),
													Container(content=self.cont_tyc),
													Container(content=self.lbl_tyc_required)
												]
											)
										)
									]
								)
							),
							Container(
								margin=margin.only(top=(SPACING / 2)),
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

	def dlg_handle_ok_button(self, _: ControlEvent) -> None:
		self.page.close(self.dlg_success)
		# self.page.splash = loading_ring
		# self.loading_ring.visible = True
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
			data = response.json()
			self.basket.email = self.txt_email.value
			self.basket.id = data["id"]
			self.basket.username = data["username"]
			self.basket.session_token = data["token"]
			self.basket.created_at = data["created_at"]

			logger.info("Cleaning text fields...")
			self.txt_username.value = ""
			self.txt_email.value = ""
			self.txt_password.value = ""
			self.txt_confirm_password.value = ""
			self.chk_tyc.value = False

			# self.page.splash = None
			# self.loading_ring.visible = False
			go_to_view(page=self.page, logger=logger, route="home")

		else:
			logger.error("An error occurred while trying to authenticate user")
			self.dlg_error.title = Text(value="Error al iniciar sesión")
			self.dlg_error.content = Text(
				value=(
					"Ocurrió un error al iniciar sesión. "
					"Favor de intentarlo de nuevo más tarde."
				)
			)
			# self.page.splash = None
			# self.loading_ring.visible = False
			self.page.open(self.dlg_error)

	def handle_btn_back(self, _: ControlEvent) -> None:
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

		go_to_view(page=self.page, logger=logger, route="") # '/'

	def btn_submit_clicked(self, _: ControlEvent) -> None:
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
				self.dlg_error.title = Text(value="Las contraseñas no coinciden")
				self.dlg_error.content = Text(value="Las contraseñas no coinciden. Favor de verificarlas.")
				self.page.open(self.dlg_error)

			elif not match(pattern=RGX_EMAIL, string=self.txt_email.value):
				logger.info("Invalid email format. Aborting process...")
				self.dlg_error.title = Text(value="Formato de correo inválido")
				self.dlg_error.content = Text(value="El correo electrónico ingresado no es válido. Favor de verificarlo.")
				self.page.open(self.dlg_error)

			# if self.lbl_pwd_match.visible == False and all([
			# 	self.txt_username.value,
			# 	match(pattern=RGX_EMAIL, string=self.txt_email.value),
			# 	self.txt_password.value,
			# 	self.txt_confirm_password.value,
			# 	self.chk_tyc.value
			# ]):
			# 	self.btn_submit.disabled = False
			# else:
			# 	self.btn_submit.disabled = True
			# self.page.update()

			else:
				logger.info("Creating new user...")
				# self.page.splash = loading_ring
				# self.loading_ring.visible = True
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
					# self.page.splash = None
					# self.loading_ring.visible = False
					self.page.open(self.dlg_success)

				elif response.status_code == 409:
					logger.error("Email already exists")
					# self.page.splash = None
					# self.loading_ring.visible = False
					self.dlg_error.title = Text(value="Error al crear usuario")
					self.dlg_error.content = Text(
						value=(
							"El correo electrónico proporcionado ya fue usado.\n"
							"Favor de usar uno diferente."
						),
					)
					self.page.open(self.dlg_error)

				else:
					logger.error("Error creating user")
					# self.page.splash = None
					# self.loading_ring.visible = False
					self.dlg_error.title = Text(value="Error al crear usuario")
					self.dlg_error.content = Text(
						value=(
							"Ocurrió un error al crear el usuario. "
							"Favor de intentarlo de nuevo más tarde."
						)
					)
					self.page.open(self.dlg_error)
