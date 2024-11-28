import flet as ft
from re import match
from typing import Any
from os.path import join
from shutil import copyfile
from requests import put, Response
from logging import Logger, getLogger

from components.bars import *
from resources.config import *
from resources.functions import go_to_view
from resources.styles import btn_primary_style, btn_secondary_style, txt_style


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class UpdateUserView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page

		# Custom components
		self.dlg_updated_data: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Datos actulizados"),
			content=ft.Text("Sus datos han sido actualizados correctamente."),
			actions=[
				ft.TextButton("Aceptar", on_click=self.handle_dlg_updated_data),
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=self.handle_dlg_updated_data
		)
		self.dlg_updated_image: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Imagen actualizada"),
			content=ft.Text("Su imagen de perfil ha sido actualizada correctamente."),
			actions=[
				ft.TextButton("Aceptar", on_click=self.handle_dlg_updated_image),
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=self.handle_dlg_updated_image
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
		self.txt_username: ft.TextField = ft.TextField(
			prefix_icon=ft.icons.ACCOUNT_CIRCLE,
			hint_text="Nuevo nombre de usuario",
			value=self.page.session.get("username"),
			**txt_style
		)
		self.txt_email: ft.TextField = ft.TextField(
			prefix_icon=ft.icons.EMAIL,
			hint_text="Nuevo correo electrónico",
			value=self.page.session.get("email"),
			**txt_style
		)
		self.txt_password: ft.TextField = ft.TextField(
			prefix_icon=ft.icons.LOCK,
			hint_text="Nueva contraseña",
			password=True,
			can_reveal_password=True,
			on_change=self.validate,
			**txt_style
		)
		self.txt_confirm_password: ft.TextField = ft.TextField(
			prefix_icon=ft.icons.LOCK,
			hint_text="Confirmar nueva contraseña",
			password=True,
			can_reveal_password=True,
			on_change=self.validate,
			**txt_style
		)
		self.lbl_pwd_match: ft.Text = ft.Text(
			value = "Las contraseñas no coinciden.",
			style=ft.TextStyle(color=ft.colors.RED),
			visible=False
		)
		self.btn_submit: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			content=ft.Text(
				value="Confirmar cambios",
				size=BTN_TEXT_SIZE
			),
			on_click=self.btn_submit_clicked,
			**btn_primary_style
		)
		self.btn_back: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			content=ft.Text(
				value="Descartar cambios",
				size=BTN_TEXT_SIZE
			),
			on_click=self.btn_back_clicked,
			**btn_secondary_style
		)
		self.dlg_user_image: ft.FilePicker = ft.FilePicker(
			on_result=self.save_new_user_image
		)
		self.page.overlay.append(self.dlg_user_image)

		# View native attributes
		super().__init__(
			route="/update_user",
			bgcolor=MAIN_COLOR,
			padding=ft.padding.all(value=0.0),
			spacing=0,
			controls=[
				TopBar(page=self.page, leading=True, logger=logger),
				ft.Container(
					width=self.page.width,
					alignment=ft.alignment.center,
					padding=ft.padding.only(
						left=SPACING,
						right=SPACING,
						bottom=SPACING,
					),
					content=ft.Stack(
						width=PROFILE_IMAGE_DIMENSIONS,
						height=PROFILE_IMAGE_DIMENSIONS,
						controls=[
							ft.CircleAvatar(
								radius=(SPACING * 4),
								foreground_image_src="/user.jpg",
								background_image_src="/user.jpg",
								content=ft.Text(
									value=self.format_image_name(self.page.session.get("username"))
								),
							),
							ft.Container(
								alignment=ft.alignment.bottom_right,
								content=ft.CircleAvatar(
									bgcolor=SECONDARY_COLOR,
									radius=SPACING,
									content=ft.IconButton(
										icon=ft.icons.EDIT,
										icon_color=ft.colors.WHITE,
										on_click=lambda _: self.dlg_user_image.pick_files(
											file_type=ft.FilePickerFileType.IMAGE,
											allowed_extensions=["jpg", "jpeg", "png"]
										)
									)
								)
							)
						]
					)
				),
				ft.Container(
					expand=True,
					width=self.page.width,
					bgcolor=ft.colors.WHITE,
					padding=ft.padding.all(value=SPACING),
					border_radius=ft.border_radius.only(
						top_left=RADIUS,
						top_right=RADIUS
					),
					shadow=ft.BoxShadow(
						blur_radius=(BLUR / 2),
						offset=ft.Offset(0, -2),
						color=ft.colors.BLACK
					),
					content=ft.Column(
						spacing=(SPACING / 2),
						controls=[
							ft.Text(
								value=(
									"Cambia o ingresa los datos que deseas actualizar.\n"
									"Los campos de contraseña pueden permanecer "
									"vacíos si no deseas cambiarlos."
								),
								color=ft.colors.BLACK
							),
							ft.Container(
								content=ft.Column(
									spacing=(SPACING / 2),
									controls=[
										ft.Container(
											height=TXT_CONT_SIZE,
											content=self.txt_username,
										),
										ft.Container(
											height=TXT_CONT_SIZE,
											content=self.txt_email,
										),
										ft.Container(
											height=TXT_CONT_SIZE,
											content=self.txt_password,
										),
										ft.Container(
											height=TXT_CONT_SIZE,
											content=self.txt_confirm_password,
										),
										ft.Container(
											content=self.lbl_pwd_match
										)
									]
								)
							),
							ft.Container(
								content=ft.Column(
									controls=[
										self.btn_submit,
										ft.Divider(color=ft.colors.TRANSPARENT),
										self.btn_back
									]
								)
							)
						]
					)
				)
			],
			bottom_appbar=BottomBar(page=self.page, logger=logger, current_route="/update_user")
		)

	def format_image_name(self, name: str) -> str:
		if " " in name:
			name, last_name = name.split(" ")
			return f"{name[0].upper()}{last_name[0].upper()}"
		else:
			return f"{name[:2].upper()}"

	def validate(self, _: ft.ControlEvent) -> None:
		if self.txt_password.value != "" or self.txt_confirm_password.value != "":
			if self.txt_password.value != self.txt_confirm_password.value:
				self.lbl_pwd_match.visible = True
			else:
				self.lbl_pwd_match.visible = False

		else:
			self.lbl_pwd_match.visible = False

		self.page.update()

	def btn_submit_clicked(self, _: ft.ControlEvent) -> None:
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
			logger.info("Submit button clicked, initiating process to update user data...")
			data_changed: bool = False
			payload: dict[str, Any] = {"mail": self.page.session.get("email")}

			logger.info("Checking what fields have changed...")
			if self.txt_email.value != self.page.session.get("email"):
				data_changed = True
				payload["mail"] = self.txt_email.value
			if self.txt_username.value != self.page.session.get("username"):
				data_changed = True
				payload["username"] = self.txt_username.value
			if self.txt_password.value != "":
				data_changed = True
				payload["password"] = self.txt_password.value

			if not data_changed:
				logger.info("No changes detected, aborting process...")
				self.dlg_error.title = ft.Text(value="Sin cambios detectados")
				self.dlg_error.content = ft.Text(value="No se detectaron cambios en tus datos. Abortando...")
				self.page.open(self.dlg_error)

			else:
				logger.info("Making request to update user...")
				response: Response = put(
					url=f"{BACK_END_URL}/{USERS_ENDPOINT}/{self.page.session.get('id')}",
					headers={
						"Content-Type": "application/json",
						"Authorization": f"Bearer {self.page.session.get('session_token')}"
					},
					json=payload
				)

				if response.status_code == 201:
					logger.info("User updated successfully")
					self.page.session.set(key="email", value=self.txt_email.value)
					self.page.session.set(key="username", value=self.txt_username.value)

					logger.info("Cleaning text fields...")
					self.txt_password.value = ""
					self.txt_confirm_password.value = ""

					self.page.open(self.dlg_updated_data)

				else:
					logger.error("Error updating user")
					self.dlg_error.title = ft.Text(value="Error al actualizar datos")
					self.dlg_error.content = ft.Text(
						value=(
							"Ocurrió un error al intentar actualizar tus datos. "
							"Favor de intentarlo de nuevo más tarde."
						)
					)

					self.page.open(self.dlg_error)

	def btn_back_clicked(self, _: ft.ControlEvent) -> None:
		logger.info("Back button clicked, discarding changes...")

		logger.info("Cleaning fields...")
		self.txt_password.value = ""
		self.txt_confirm_password.value = ""

		go_to_view(page=self.page, logger=logger, route="/account")

	def save_new_user_image(self, event: ft.FilePickerResultEvent) -> None:
		logger.info("Processing new image selected...")

		if event.files:
			if event.files[0].path:
				logger.info("Saving new image...")
				extension: str = event.files[0].name.split(".")[-1]
				copyfile(event.files[0].path, join(ASSETS_ABSPATH, f"user.{extension}"))
				logger.info("New image saved successfully.")

				self.page.open(self.dlg_updated_image)

			else:
				logger.error("Error saving new image.")
				self.dlg_error.title = ft.Text(value="Error al guardar la nueva imagen")
				self.dlg_error.content = ft.Text(
					value=(
						"Ocurrió un error al intentar guardar la nueva imagen. "
						"Favor de intentarlo de nuevo más tarde."
					)
				)

				self.page.open(self.dlg_error)
		else:
			logger.info("No image selected. Aborting...")

	def handle_dlg_updated_data(self, _: ft.ControlEvent) -> None:
		self.page.close(self.dlg_updated_data)
		go_to_view(page=self.page, logger=logger, route="/account")

	def handle_dlg_updated_image(self, _: ft.ControlEvent) -> None:
		self.page.close(self.dlg_updated_image)

		go_to_view(page=self.page, logger=logger, route="/account")
