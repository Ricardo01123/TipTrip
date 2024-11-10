from flet import *
from logging import getLogger
from requests import post, Response
from flet_route import Params, Basket

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

		self.lbl_email_required: Text = Text(
			value = "Campo \"Correo electrónico\" requerido *",
			style=TextStyle(color=colors.RED),
			visible=False
		)

		self.lbl_password_required: Text = Text(
			value = "Campo \"Contraseña\" requerido *",
			style=TextStyle(color=colors.RED),
			visible=False
		)

		self.dlg_not_found: AlertDialog = AlertDialog(
			modal=True,
			title=Text("Usuario no encontrado"),
			content=Text("Usuario y/o contraseña incorrectos."),
			actions=[
				TextButton("Aceptar", on_click=lambda _: self.page.close(self.dlg_not_found)),
			],
			actions_alignment=MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_not_found)
		)

		self.dlg_error: AlertDialog = AlertDialog(
			modal=True,
			title=Text("Error al iniciar sesión"),
			content=Text(
				"Ocurrió un error al intentar iniciar sesión. "
				"Favor de intentarlo de nuevo más tarde."
			),
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
								margin=margin.only(top=(SPACING * 2)),
								content=Column(
									spacing=(SPACING / 2),
									controls=[
										Container(
											height=TXT_CONT_SIZE,
											content=self.txt_email
										),
										Container(content=self.lbl_email_required),
										Container(
											height=TXT_CONT_SIZE,
											content=self.txt_password
										),
										Container(content=self.lbl_password_required),
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
									md_style_sheet=MarkdownStyleSheet(
										p_text_style=TextStyle(color=colors.BLACK)
									),
									on_tap_link=lambda _: go_to_view(
										page=self.page,
										logger=logger,
										route="privacy_politics"
									)
								)
							)
						]
					),
					**cont_main_style
				)
			]
		)

	def btn_submit_clicked(self, _: ControlEvent) -> None:
		email_txt_filled: bool = False
		password_txt_filled: bool = False

		logger.info("Checking if login fields are filled...")
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

		self.page.update()

		if email_txt_filled and password_txt_filled:
			logger.info("Checking if credentials exists in DB...")
			response: Response = post(
				url=f"{BACK_END_URL}/{AUTH_USER_ENDPOINT}",
				headers={"Content-Type": "application/json"},
				json={
					"mail": self.txt_email.value,
					"password": self.txt_password.value
				}
			)

			if response.status_code == 201:
				data: dict = response.json()
				logger.info("User authenticated successfully")

				logger.info("Adding user data to session data...")
				self.basket.id = data["id"]
				self.basket.email = self.txt_email.value
				self.basket.username = data["username"]
				self.basket.session_token = data["token"]
				self.basket.created_at = data["created_at"]

				logger.info("Cleaning text fields...")
				self.txt_email.value = ""
				self.txt_password.value = ""

				go_to_view(page=self.page, logger=logger, route="home")

			elif response.status_code == 401 or response.status_code == 404:
				logger.info("User and/or password are incorrect")
				self.page.open(self.dlg_not_found)

			else:
				logger.error("An error occurred while authenticating the user")
				self.page.open(self.dlg_error)
