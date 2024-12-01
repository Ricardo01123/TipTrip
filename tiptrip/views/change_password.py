import flet as ft
from requests import put, Response
from logging import Logger, getLogger

from resources.config import *
from resources.styles import *
from resources.functions import *
from components.splash import Splash
from components.titles import MainTitle


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class ChangePasswordView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page

		# Custom components
		self.txt_password: ft.TextField = ft.TextField(
			prefix_icon=ft.Icons.LOCK,
			hint_text="Contraseña",
			password=True,
			can_reveal_password=True,
			on_change=self.validate,
			**txt_style
		)
		self.txt_confirm_password: ft.TextField = ft.TextField(
			prefix_icon=ft.Icons.LOCK,
			hint_text="Confirmar contraseña",
			password=True,
			can_reveal_password=True,
			on_change=self.validate,
			**txt_style
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
		self.dlg_updated_data: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Contraseña actualizada"),
			content=ft.Text("La contraseña ha sido actualizada correctamente."),
			actions=[
				ft.TextButton("Aceptar", on_click=self.handle_dlg_updated_data),
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=self.handle_dlg_updated_data
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
			text="Cambiar contraseña",
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
			route="/change_password",
			bgcolor=MAIN_COLOR,
			padding=ft.padding.all(value=0.0),
			controls=[
				ft.Container(
					expand=True,
					content=ft.Stack(
						controls=[
							ft.Container(
								height=self.page.height,
								scroll=ft.ScrollMode.HIDDEN,
								content=ft.Column(
									controls=[
										ft.Container(
											content=ft.IconButton(
												icon=ft.Icons.ARROW_BACK,
												icon_color=ft.Colors.BLACK,
												on_click=lambda _: go_to_view(page=self.page, logger=logger, route="/sign_in")
											)
										),
										MainTitle(
											subtitle="Cambiar contraseña",
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
																"Ingresa una nueva contraseña:"
															),
															color=ft.Colors.BLACK
														)
													),
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
													ft.Container(content=self.lbl_pwd_match)
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

	def btn_back_clicked(self, _: ft.ControlEvent) -> None:
		self.txt_password.value = ""
		self.txt_confirm_password.value = ""
		self.lbl_password_required.visible = False
		self.lbl_confirm_password_required.visible = False
		self.page.update()

		logger.info("Showing loading splash screen...")
		self.cont_splash.visible = True
		self.splash.visible = True
		self.page.update()

		go_to_view(page=self.page, logger=logger, route="/sign_in")

		logger.info("Hidding loading splash screen...")
		self.cont_splash.visible = False
		self.splash.visible = False
		self.page.update()

	def btn_submit_clicked(self, _: ft.ControlEvent) -> None:
		if (self.txt_password.value == "" or self.txt_password.value.isspace()) or \
			(self.txt_confirm_password.value == "" or self.txt_confirm_password.value.isspace()):

			if self.txt_password.value == "" or self.txt_password.value.isspace():
				logger.warning("Empty password field. Updating view...")
				self.lbl_password_required.visible = True
				self.page.update()

			if self.txt_confirm_password.value == "" or self.txt_confirm_password.value.isspace():
				logger.warning("Empty confirm password field. Updating view...")
				self.lbl_confirm_password_required.visible = True
				self.page.update()

		else:
			if not self.lbl_pwd_match.visible:
				logger.info("Showing loading splash screen...")
				self.cont_splash.visible = True
				self.splash.visible = True
				self.page.update()

				logger.info("Updating user password...")
				response: Response = put(
					url=f"{BACK_END_URL}/{USERS_ENDPOINT}/{self.page.session.get('id')}",
					headers={
						"Content-Type": "application/json",
						"Authorization": f"Bearer {self.page.session.get('session_token')}"
					},
					json={"password": self.txt_password.value.strip()}
				)

				if response.status_code == 201:
					logger.info("Password updated successfully. Updating view...")
					self.cont_splash.visible = False
					self.splash.visible = False
					self.txt_password.value = ""
					self.txt_confirm_password.value = ""
					self.lbl_password_required.visible = False
					self.lbl_confirm_password_required.visible = False
					self.page.update()

					self.page.open(self.dlg_updated_data)

				else:
					logger.error("Error verifying user")
					logger.info(f"Response: {response.json()}")
					self.dlg_error.title = ft.Text(value="Error al verificar usuario")
					self.dlg_error.content = ft.Text(
						value=(
							"Ocurrió un error al cambiar la contraseña. "
							"Favor de intentarlo de nuevo más tarde."
						)
					)
					logger.info("Hidding loading splash screen...")
					self.cont_splash.visible = False
					self.splash.visible = False
					self.txt_password.value = ""
					self.txt_confirm_password.value = ""
					self.lbl_password_required.visible = False
					self.lbl_confirm_password_required.visible = False
					self.page.update()

					self.page.open(self.dlg_error)

	def handle_dlg_updated_data(self, _: ft.ControlEvent) -> None:
		self.page.close(self.dlg_updated_data)

		logger.info("Showing loading splash screen...")
		self.cont_splash.visible = True
		self.splash.visible = True
		self.page.update()

		go_to_view(page=self.page, logger=logger, route="/sign_in")

		logger.info("Hidding loading splash screen...")
		self.cont_splash.visible = False
		self.splash.visible = False
		self.page.update()
