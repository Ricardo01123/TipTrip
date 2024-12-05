import flet as ft
from re import match
from typing import Any
from os.path import join
from shutil import copyfile
from logging import Logger, getLogger

from requests import put, Response
from requests.exceptions import ConnectTimeout

from components.bars import *
from resources.config import *
from resources.functions import go_to_view, get_user_image
from resources.styles import btn_primary_style, btn_secondary_style, txt_style


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class UpdateUserView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page
		self.user_image: str = get_user_image()

		# Custom components
		self.dlg_updated_data: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Datos actualizados"),
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
			prefix_icon=ft.Icons.ACCOUNT_CIRCLE,
			label="Nuevo nombre de usuario",
			hint_text="Fernanda",
			autofocus=True,
			value=self.page.session.get("username"),
			**txt_style
		)
		self.txt_email: ft.TextField = ft.TextField(
			prefix_icon=ft.Icons.EMAIL,
			label="Nuevo correo electrónico",
			hint_text="ejemplo@ejemplo.com",
			value=self.page.session.get("email"),
			**txt_style
		)
		self.txt_password: ft.TextField = ft.TextField(
			prefix_icon=ft.Icons.LOCK,
			label="Nueva contraseña",
			password=True,
			can_reveal_password=True,
			on_change=self.validate,
			**txt_style
		)
		self.txt_confirm_password: ft.TextField = ft.TextField(
			prefix_icon=ft.Icons.LOCK,
			label="Confirmar nueva contraseña",
			password=True,
			can_reveal_password=True,
			on_change=self.validate,
			**txt_style
		)
		self.lbl_pwd_match: ft.Text = ft.Text(
			value = "Las contraseñas no coinciden.",
			style=ft.TextStyle(color=ft.Colors.RED),
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
						height=((PROFILE_IMAGE_DIMENSIONS * 2) + SPACING),
						controls=[
							ft.Container(
								width=self.page.width,
								height=(PROFILE_IMAGE_DIMENSIONS * 2) + SPACING,
								alignment=ft.alignment.center,
								padding=ft.padding.only(bottom=SPACING),
								content=(
									ft.Image(
										width=(PROFILE_IMAGE_DIMENSIONS * 2),
										height=(PROFILE_IMAGE_DIMENSIONS * 2),
										src=self.user_image,
										fit=ft.ImageFit.FILL,
										repeat=ft.ImageRepeat.NO_REPEAT,
										border_radius=ft.border_radius.all(value=PROFILE_IMAGE_DIMENSIONS),
										error_content=ft.Icon(
											name=ft.Icons.ACCOUNT_CIRCLE,
											color=ft.Colors.BLACK,
											size=(PROFILE_IMAGE_DIMENSIONS * 2),
										)
									)
								)
							),
							ft.Container(
								expand=True,
								right=(SPACING * 4),
								bottom=(SPACING * 2),
								content=ft.CircleAvatar(
									bgcolor=SECONDARY_COLOR,
									radius=(SPACING * 2),
									content=ft.IconButton(
										icon=ft.Icons.EDIT,
										icon_color=ft.Colors.WHITE,
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
					bgcolor=ft.Colors.WHITE,
					padding=ft.padding.all(value=SPACING),
					border_radius=ft.border_radius.only(
						top_left=RADIUS,
						top_right=RADIUS
					),
					shadow=ft.BoxShadow(
						blur_radius=(BLUR / 2),
						offset=ft.Offset(0, -2),
						color=ft.Colors.BLACK
					),
					content=ft.Column(
						scroll=ft.ScrollMode.HIDDEN,
						spacing=(SPACING / 2),
						controls=[
							ft.Text(
								value=(
									"Cambia o ingresa los datos que deseas actualizar. "
									"Los campos de contraseña pueden permanecer "
									"vacíos si no deseas cambiarlos."
								),
								color=ft.Colors.BLACK,
								text_align=ft.TextAlign.JUSTIFY
							),
							ft.Container(
								content=ft.Column(
									# spacing=(SPACING / 2),
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

		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()

	def btn_submit_clicked(self, _: ft.ControlEvent) -> None:
		if self.lbl_pwd_match.visible:
			logger.info("Passwords do not match. Aborting process...")
			self.dlg_error.title = ft.Text(value="Las contraseñas no coinciden")
			self.dlg_error.content = ft.Text(value="Las contraseñas no coinciden. Favor de verificarlas.")

			try:
				self.page.open(self.dlg_error)
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.open(self.dlg_error)

		elif not match(pattern=RGX_EMAIL, string=self.txt_email.value):
			logger.info("Invalid email format. Aborting process...")
			self.dlg_error.title = ft.Text(value="Formato de correo inválido")
			self.dlg_error.content = ft.Text(value="El correo electrónico ingresado no es válido. Favor de verificarlo.")
			try:
				self.page.open(self.dlg_error)
			except Exception as e:
				logger.error(f"Error: {e}")
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
				try:
					self.page.open(self.dlg_error)
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.open(self.dlg_error)

			else:
				logger.info("Making request to update user...")
				try:
					response: Response = put(
						url=f"{BACK_END_URL}/{USERS_ENDPOINT}/{self.page.session.get('id')}",
						headers={
							"Content-Type": "application/json",
							"Authorization": f"Bearer {self.page.session.get('session_token')}"
						},
						json=payload
					)

				except ConnectTimeout:
					logger.error("Connection timeout while updating user")
					self.dlg_error.title = ft.Text(value="Error de conexión a internet")
					self.dlg_error.content = ft.Text(
						value=(
							"No se pudieron actualizar los datos. "
							"Favor de revisar tu conexión a internet e intentarlo de nuevo más tarde."
						)
					)

					try:
						self.page.open(self.dlg_error)

					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.open(self.dlg_error)

					finally:
						return

				if response.status_code == 201:
					logger.info("User updated successfully")
					self.page.session.set(key="email", value=self.txt_email.value)
					self.page.session.set(key="username", value=self.txt_username.value)

					logger.info("Cleaning text fields...")
					self.txt_password.value = ""
					self.txt_confirm_password.value = ""

					try:
						self.page.open(self.dlg_updated_data)
					except Exception as e:
						logger.error(f"Error: {e}")
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

					try:
						self.page.open(self.dlg_error)
					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.open(self.dlg_error)

	def btn_back_clicked(self, _: ft.ControlEvent) -> None:
		logger.info("Back button clicked, discarding changes...")

		logger.info("Cleaning fields...")
		self.txt_password.value = ""
		self.txt_confirm_password.value = ""

		try:
			go_to_view(page=self.page, logger=logger, route="/account")
		except Exception as e:
			logger.error(f"Error: {e}")
			go_to_view(page=self.page, logger=logger, route="/account")

	def save_new_user_image(self, event: ft.FilePickerResultEvent) -> None:
		logger.info("Processing new image selected...")

		if event.files:
			if event.files[0].path:
				logger.info("Saving new image...")
				extension: str = event.files[0].name.split(".")[-1]
				copyfile(event.files[0].path, join(ASSETS_ABSPATH, f"user.{extension}"))
				logger.info("New image saved successfully.")

				try:
					self.page.open(self.dlg_updated_image)
				except Exception as e:
					logger.error(f"Error: {e}")
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
				try:
					self.page.open(self.dlg_error)
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.open(self.dlg_error)

		else:
			logger.info("No image selected. Aborting...")

	def handle_dlg_updated_data(self, _: ft.ControlEvent) -> None:
		try:
			self.page.close(self.dlg_updated_data)
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.close(self.dlg_updated_data)

		try:
			go_to_view(page=self.page, logger=logger, route="/account")
		except Exception as e:
			logger.error(f"Error: {e}")
			go_to_view(page=self.page, logger=logger, route="/account")

	def handle_dlg_updated_image(self, _: ft.ControlEvent) -> None:
		try:
			self.page.close(self.dlg_updated_image)
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.close(self.dlg_updated_image)

		try:
			go_to_view(page=self.page, logger=logger, route="/account")
		except Exception as e:
			logger.error(f"Error: {e}")
			go_to_view(page=self.page, logger=logger, route="/account")
