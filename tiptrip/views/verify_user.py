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


class VerifyUserView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page

		# Custom components
		self.txt_email: ft.TextField = ft.TextField(
			prefix_icon=ft.Icons.EMAIL,
			label="Correo electrónico",
			hint_text="ejemplo@ejemplo.com",
			autofocus=True,
			**txt_style
		)
		self.lbl_email_required: ft.Text = ft.Text(
			value = "Campo requerido *",
			style=ft.TextStyle(color=ft.Colors.RED),
			visible=False
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
			text="Verificar",
			on_click=self.btn_submit_clicked,
			**btn_primary_style
		)
		self.btn_back: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			content=ft.Text(value="Regresar a Iniciar sesión", size=BTN_TEXT_SIZE),
			on_click=self.btn_back_clicked,
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
			route="/verify_user",
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
												on_click=lambda _: go_to_view(page=self.page, logger=logger, route="/sign_in")
											)
										),
										MainTitle(
											subtitle="Verificar usuario",
											top_margin=10
										),
										ft.Container(
											expand=True,
											margin=ft.margin.only(top=(SPACING * 2)),
											content=ft.Column(
												controls=[
													ft.Container(
														content=ft.Text(
															value=(
																"Verifica tu correo electrónico "
																"para cambiar tu contraseña:"
															),
															color=ft.Colors.BLACK
														)
													),
													ft.Container(
														height=TXT_CONT_SIZE,
														content=self.txt_email,
													),
													ft.Container(content=self.lbl_email_required)
												]
											)
										),
										ft.Container(
											margin=ft.margin.symmetric(vertical=SPACING),
											content=ft.Column(
												controls=[
													self.btn_submit,
													ft.Divider(color=ft.Colors.TRANSPARENT),
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

	def btn_back_clicked(self, _: ft.ControlEvent) -> None:
		self.txt_email.value = ""
		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()
			#! COMMENT
			post(
				url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
				headers={"Content-Type": "application/json"},
				json={
					"user_id": self.page.session.get("id"),
					"file": encode_logfile()
				}
			)

		try:
			go_to_view(page=self.page, logger=logger, route="/sign_in")
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
			go_to_view(page=self.page, logger=logger, route="/sign_in")

	def btn_submit_clicked(self, _: ft.ControlEvent) -> None:
		if self.txt_email.value == "" or self.txt_email.value.isspace():
			logger.warning("Empty mail field. Updating view...")
			self.lbl_email_required.visible = True
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

		elif not match(pattern=RGX_EMAIL, string=self.txt_email.value):
			logger.warning("Invalid email format")
			self.dlg_error.title = ft.Text(value="Formato de correo inválido")
			self.dlg_error.content = ft.Text(value="El correo electrónico ingresado no es válido. Favor de verificarlo.")
			try:
				self.page.open(self.dlg_error)
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.open(self.dlg_error)
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

		else:
			logger.info("Showing loading splash screen...")
			self.cont_splash.visible = True
			self.splash.visible = True
			self.lbl_email_required.visible = False
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

			logger.info("Verifying user...")
			try:
				response: Response = post(
					url=f"{BACK_END_URL}/{USERS_ENDPOINT}/verify",
					headers={"Content-Type": "application/json"},
					json={"mail": self.txt_email.value.strip()}
				)

			except ConnectTimeout:
				logger.error("Connection timeout while verifying user")
				self.dlg_error.title = ft.Text(value="Error de conexión a internet")
				self.dlg_error.content = ft.Text(
					value=(
						"No se pudo verificar el usuario. "
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
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)
					return

			if response.status_code == 201:
				logger.info("User verified successfully")
				data: dict = response.json()

				self.txt_email.value = ""
				try:
					self.page.update()
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.update()
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

				logger.info("Setting session data...")
				self.page.session.set(key="aux", value=None) # This is a workaround to avoid a bug in the framework
				self.page.session.set(key="id", value=data["id"])
				self.page.session.set(key="session_token", value=data["token"])

				logger.info("Hidding loading splash screen...")
				self.cont_splash.visible = False
				self.splash.visible = False
				try:
					self.page.update()
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.update()
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

				try:
					go_to_view(page=self.page, logger=logger, route="/change_password")
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
					go_to_view(page=self.page, logger=logger, route="/change_password")

			elif response.status_code == 404:
				logger.warning("User not found")
				self.dlg_error.title = ft.Text(value="Usuario no encontrado")
				self.dlg_error.content = ft.Text(
					value=(
						"El correo electrónico ingresado no se encuentra registrado. "
						"Favor de verificarlo."
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
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

				try:
					self.page.open(self.dlg_error)
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.open(self.dlg_error)
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

			else:
				logger.error("Error verifying user")
				self.dlg_error.title = ft.Text(value="Error al verificar usuario")
				self.dlg_error.content = ft.Text(
					value=(
						"Ocurrió un error al verificar usuario. "
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
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

				try:
					self.page.open(self.dlg_error)
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.open(self.dlg_error)
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)
