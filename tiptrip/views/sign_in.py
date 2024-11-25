import flet as ft
from requests import post, Response
from logging import Logger, getLogger

from resources.config import *
from resources.styles import *
from resources.functions import *
from components.titles import MainTitle


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class SignInView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page
		self.gl: ft.Geolocator = ft.Geolocator(
			location_settings=ft.GeolocatorSettings(
				accuracy=ft.GeolocatorPositionAccuracy.LOW
			),
			on_error=lambda error: logger.error(f"Geolocator error: {error}"),
		)
		self.page.overlay.append(self.gl)

		# Custom components
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
			**txt_style
		)
		self.lbl_email_required: ft.Text = ft.Text(
			value="Campo requerido *",
			style=ft.TextStyle(color=ft.colors.RED),
			visible=False
		)
		self.lbl_password_required: ft.Text = ft.Text(
			value="Campo requerido *",
			style=ft.TextStyle(color=ft.colors.RED),
			visible=False
		)
		self.dlg_not_found: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Usuario no encontrado"),
			content=ft.Text("Usuario y/o contraseña incorrectos."),
			actions=[
				ft.TextButton("Aceptar", on_click=lambda _: self.page.close(self.dlg_not_found)),
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_not_found)
		)
		self.dlg_error: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Error al iniciar sesión"),
			content=ft.Text(
				"Ocurrió un error al intentar iniciar sesión. "
				"Favor de intentarlo de nuevo más tarde."
			),
			actions=[
				ft.TextButton("Aceptar", on_click=lambda _: self.page.close(self.dlg_error)),
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_error)
		)
		self.btn_submit: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			content=ft.Text(value="Iniciar sesión", size=BTN_TEXT_SIZE),
			on_click=self.btn_submit_clicked,
			**btn_primary_style
		)
		self.btn_sign_up: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			content=ft.Text(value="Registrarse", size=BTN_TEXT_SIZE),
			on_click=lambda _: go_to_view(page=self.page, logger=logger, route="/sign_up"),
			**btn_secondary_style,
		)

		# View native attributes
		super().__init__(
			route="/sign_in",
			bgcolor=MAIN_COLOR,
			padding=ft.padding.all(value=0.0),
			controls=[
				ft.Container(
					content=ft.Column(
						scroll=ft.ScrollMode.HIDDEN,
						controls=[
							MainTitle(
								subtitle="Iniciar sesión",
								top_margin=(SPACING * 2),
							),
							ft.Container(
								margin=ft.margin.only(top=(SPACING * 2)),
								content=ft.Column(
									spacing=(SPACING / 2),
									controls=[
										ft.Container(
											height=TXT_CONT_SIZE,
											content=self.txt_email
										),
										ft.Container(content=self.lbl_email_required),
										ft.Container(
											height=TXT_CONT_SIZE,
											content=self.txt_password
										),
										ft.Container(content=self.lbl_password_required),
										ft.Container(
											content=ft.TextButton(
												content=ft.Container(
													content=ft.Text(
														value="¿Olvidaste tu contraseña?",
														color=ft.colors.BLACK
													)
												),
												on_click=lambda _: go_to_view(page=self.page, logger=logger, route="/change_password")
											)
										)
									]
								)
							),
							ft.Container(
								margin=ft.margin.only(top=(SPACING * 3)),
								content=ft.Column(
									controls=[
										self.btn_submit,
										ft.Divider(color=ft.colors.TRANSPARENT),
										self.btn_sign_up
									]
								)
							),
							ft.Container(
								margin=ft.margin.only(top=(SPACING * 2)),
								content=ft.Markdown(
									value=(
										"Para conocer más acerca de nuestra "
										"Política de Privacidad da click "
										"[aquí](https://www.google.com)."
									),
									md_style_sheet=ft.MarkdownStyleSheet(
										p_text_style=ft.TextStyle(color=ft.colors.BLACK)
									),
									on_tap_link=lambda _: go_to_view(page=self.page, logger=logger, route="/privacy_politics")
								)
							)
						]
					),
					**cont_main_style
				)
			]
		)

	def btn_submit_clicked(self, _: ft.ControlEvent) -> None:
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
				data: dict = response.json()

				logger.info("Adding user data to session data...")
				self.page.session.set(key="id", value=data["id"])
				self.page.session.set(key="email", value=self.txt_email.value)
				self.page.session.set(key="username", value=data["username"])
				self.page.session.set(key="session_token", value=data["token"])
				self.page.session.set(key="created_at", value=data["created_at"])
				# Creating session environment variables
				# Home variables
				self.page.session.set(key="places_data", value=None)
				self.page.session.set(key="sld_value", value=7)
				self.page.session.set(key="drd_classification_value", value="")
				self.page.session.set(key="drd_municipality_value", value="")
				# Map variables
				self.page.session.set(key="map_places_data", value=None)
				self.page.session.set(key="map_sld_value", value=7)
				self.page.session.set(key="map_drd_value", value="")

				logger.info("Cleaning text fields...")
				self.txt_email.value = ""
				self.txt_password.value = ""

				logger.info("Checking location permissions...")
				if request_location_permissions(self.gl, logger):
					logger.info("Location permissions granted. Getting current coordinates...")
					current_position: ft.GeolocatorPosition = self.gl.get_current_position()
					self.page.session.set(key="current_latitude", value=current_position.latitude)
					self.page.session.set(key="current_longitude", value=current_position.longitude)
					logger.info(f"Got current coordinates: ({current_position.latitude}, {current_position.longitude})")

					go_to_view(page=self.page, logger=logger, route='/')

				else:
					logger.warning("Location permissions are not granted")
					go_to_view(page=self.page, logger=logger, route="/permissions")

			elif response.status_code == 401 or response.status_code == 404:
				logger.warning("User and/or password are incorrect")
				self.page.open(self.dlg_not_found)

			else:
				logger.error("An error occurred while authenticating the user")
				self.page.open(self.dlg_error)
