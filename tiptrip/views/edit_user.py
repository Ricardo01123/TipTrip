from re import match
from time import sleep
from logging import getLogger
from requests import Response, patch
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Text, Stack, CircleAvatar, ElevatedButton,
	IconButton, alignment, Offset, padding, BoxShadow, border_radius, colors,
	ControlEvent, AlertDialog, TextButton, icons, TextStyle, Banner, ButtonStyle,
	Icon, Divider, TextField
)

from components.bars import *
from resources.config import *
from resources.functions import go_to_view
from resources.styles import btn_primary_style, btn_secondary_style, txt_style


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class EditUserView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None
		self.route = None
		self.txt_username = None
		self.txt_email = None
		self.txt_password = None
		self.txt_confirm_password = None

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
					# on_click=self.bnr_handle_dismiss
				)
			],
			force_actions_below=True
		)

		self.dlg_success: AlertDialog = AlertDialog(
			modal=True,
			title=Text("Datos actualizados"),
			content=Text("Sus datos se han actualizado correctamente."),
			actions=[
				TextButton("Aceptar", on_click=self.dlg_handle_ok_button),
			],
			actions_alignment=MainAxisAlignment.END,
			on_dismiss=self.dlg_handle_dismiss
		)

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.route = "/edit_user"

		self.txt_username: TextField = TextField(
			prefix_icon=icons.ACCOUNT_CIRCLE,
			hint_text="Nuevo nombre de usuario",
			value=self.basket.get("username"),
			on_change=self.validate,
			**txt_style
		)

		self.txt_email: TextField = TextField(
			prefix_icon=icons.EMAIL,
			hint_text="Nuevo correo electrónico",
			value=self.basket.get("email"),
			on_change=self.validate,
			**txt_style
		)

		self.txt_password: TextField = TextField(
			prefix_icon=icons.LOCK,
			hint_text="Nueva contraseña",
			password=True,
			can_reveal_password=True,
			on_change=self.validate,
			**txt_style
		)

		self.txt_confirm_password: TextField = TextField(
			prefix_icon=icons.LOCK,
			hint_text="Confirmar nueva contraseña",
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

		self.btn_submit: ElevatedButton = ElevatedButton(
			width=self.page.width,
			content=Text(
				value="Confirmar cambios",
				size=BTN_TEXT_SIZE
			),
			# disabled=True,
			on_click=self.btn_submit_clicked,
			**btn_primary_style
		)

		self.btn_back: ElevatedButton = ElevatedButton(
			width=self.page.width,
			content=Text(
				value="Descartar cambios",
				size=BTN_TEXT_SIZE
			),
			on_click=self.btn_back_clicked,
			**btn_secondary_style
		)

		return View(
			route=self.route,
			bgcolor=MAIN_COLOR,
			padding=padding.all(value=0.0),
			spacing=0,
			controls=[
				TopBar(page=self.page, leading=True, logger=logger),
				Container(
					width=self.page.width,
					alignment=alignment.center,
					padding=padding.only(
						left=SPACING,
						right=SPACING,
						bottom=SPACING,
					),
					content=Stack(
						width=PROFILE_IMAGE_DIMENSIONS,
						height=PROFILE_IMAGE_DIMENSIONS,
						controls=[
							CircleAvatar(
								radius=(SPACING * 4),
								foreground_image_src="/user.jpg",
								background_image_src="/user.jpg",
								content=Text(
									value=self.format_image_name(self.basket.get("username"))
								),
							),
							Container(
								alignment=alignment.bottom_right,
								content=CircleAvatar(
									bgcolor=SECONDARY_COLOR,
									radius=SPACING,
									content=IconButton(
										icon=icons.EDIT,
										icon_color=colors.WHITE
									)
								)
							)
						]
					)
				),
				Container(
					expand=True,
					width=self.page.width,
					bgcolor=colors.WHITE,
					padding=padding.all(value=SPACING),
					border_radius=border_radius.only(
						top_left=RADIUS,
						top_right=RADIUS
					),
					shadow=BoxShadow(
						blur_radius=(BLUR / 2),
						offset=Offset(0, -2),
						color=colors.BLACK
					),
					content=Column(
						spacing=(SPACING / 2),
						controls=[
							Text(
								value=(
									"Cambia o ingresa los datos que deseas actualizar.\n"
									"Los campos de contraseña pueden permanecer "
									"vacíos si no deseas cambiarlos."
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
										)
									]
								)
							),
							Container(
								content=Column(
									controls=[
										self.btn_submit,
										Divider(color=colors.TRANSPARENT),
										self.btn_back
									]
								)
							)
						]
					)
				),
				BottomBar(
					page=self.page,
					logger=logger,
					current_route=self.route
				)
			]
		)

	def format_image_name(self, name: str) -> str:
		if " " in name:
			name, last_name = name.split(" ")
			return f"{name[0].upper()}{last_name[0].upper()}"
		else:
			return f"{name[:2].upper()}"

	def validate(self, event: ControlEvent) -> None:
		if self.txt_password.value != "" or self.txt_confirm_password.value != "":
			if self.txt_password.value != self.txt_confirm_password.value:
				self.lbl_pwd_match.visible = True
				self.btn_submit.disabled = True
			else:
				self.lbl_pwd_match.visible = False
				self.btn_submit.disabled = False

		if self.lbl_pwd_match.visible == False and all([
			self.txt_username.value,
			match(pattern=RGX_EMAIL, string=self.txt_email.value)
		]):
			self.btn_submit.disabled = False
		else:
			self.btn_submit.disabled = True
		self.page.update()

	def dlg_handle_ok_button(self, event: ControlEvent) -> None:
		self.page.close(self.dlg_success)
		go_to_view(page=self.page, logger=logger, route="account")

	def dlg_handle_dismiss(self, event: ControlEvent) -> None:
		self.page.close(self.dlg_success)

	def btn_submit_clicked(self, event: ControlEvent) -> None:
		logger.info("Submit button clicked, initiating process to update user data...")

		payload = {"email": self.basket.get("email")}

		logger.info("Checking what fields have changed...")
		if self.txt_email.value != self.basket.get("email"):
			payload["new_email"] = self.txt_email.value
		if self.txt_username.value != self.basket.get("username"):
			payload["new_username"] = self.txt_username.value
		if self.txt_password.value != "":
			payload["new_password"] = self.txt_password.value

		if len(payload) == 1:
			logger.info("No changes detected, aborting process...")
			self.bnr_error.content = Text(
				value="No se detectaron cambios en tus datos.\nAbandonando proceso...",
				style=TextStyle(color=colors.RED)
			)

			self.page.open(self.bnr_error)
			sleep(3)
			self.page.close(self.bnr_error)

			go_to_view(page=self.page, logger=logger, route="account")

		else:
			logger.info("Making request to update user...")
			response: Response = patch(
				url=f"{BACK_END_URL}/{UPDATE_USER_ENDPOINT}",
				headers={
					"Content-Type": "application/json",
					"Authorization": f"Bearer {self.basket.get('session_token')}"
				},
				json=payload
			)

			if response.status_code == 201:
				logger.info("User updated successfully")
				self.basket.email = self.txt_email.value
				self.basket.username = self.txt_username.value

				logger.info("Cleaning text fields...")
				self.txt_password.value = ""
				self.txt_confirm_password.value = ""

				self.page.open(self.dlg_success)

			else:
				logger.error("Error updating user")
				self.bnr_error.content = Text(
					value=(
						"Ocurrió un error al intentar actualizar tus datos. "
						"Favor de intentarlo de nuevo más tarde."
					)
				)
				self.page.open(self.bnr_error)

	def btn_back_clicked(self, event: ControlEvent) -> None:
		logger.info("Back button clicked, discarding changes...")

		logger.info("Cleaning fields...")
		self.txt_password.value = ""
		self.txt_confirm_password.value = ""

		go_to_view(page=self.page, logger=logger, route="account")
