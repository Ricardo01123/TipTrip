import flet as ft
from re import match
from logging import Logger, getLogger

from resources.config import *
from resources.styles import *
from resources.functions import *
from components.titles import MainTitle


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class ChangePasswordView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page

		# Custom components
		self.txt_email: ft.TextField = ft.TextField(
			prefix_icon=ft.icons.EMAIL,
			hint_text="Correo electrónico",
			on_change=self.validate,
			**txt_style
		)
		self.txt_password: ft.TextField = ft.TextField(
			prefix_icon=ft.icons.LOCK,
			hint_text="Contraseña",
			password=True,
			can_reveal_password=True,
			**txt_style
		)
		self.txt_confirm_password: ft.TextField = ft.TextField(
			prefix_icon=ft.icons.LOCK,
			hint_text="Confirmar contraseña",
			password=True,
			can_reveal_password=True,
			**txt_style
		)
		self.lbl_email_required: ft.Text = ft.Text(
			value = "Campo requerido *",
			style=ft.TextStyle(color=ft.colors.RED),
			visible=False
		)
		self.cont_email: ft.Container = ft.Container(
			content=ft.Column(
				controls=[
					ft.Container(
						content=ft.Text(
							value=(
								"Verifica tu correo electrónico "
								"para cambiar tu contraseña:"
							),
							color=ft.colors.BLACK
						)
					),
					ft.Container(
						height=TXT_CONT_SIZE,
						content=self.txt_email,
					)
				]
			)
		)
		self.cont_password: ft.Container = ft.Container(
			visible=False,
			content=ft.Column(
				controls=[
					ft.Container(
						content=ft.Text(
							value="Ingresa una contraseña nueva:",
							color=ft.colors.BLACK
						)
					),
					ft.Container(
						height=TXT_CONT_SIZE,
						content=self.txt_password,
					)
				]
			)
		)
		self.cont_confirm_password: ft.Container = ft.Container(
			visible=False,
			content=ft.Column(
				controls=[
					ft.Container(
						content=ft.Text(
							value="Confirmar contraseña nueva:",
							color=ft.colors.BLACK
						)
					),
					ft.Container(
						height=TXT_CONT_SIZE,
						content=self.txt_confirm_password,
					)
				]
			)
		)
		self.btn_submit: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			text="Continuar",
			disabled=True,
			on_click=self.btn_submit_clicked,
			**btn_primary_style
		)
		self.btn_back: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			content=ft.Text(value="Regresar a Iniciar sesión", size=BTN_TEXT_SIZE),
			on_click=self.btn_back_clicked,
			**btn_secondary_style
		)

		# View native attributes
		super().__init__(
			route="/change_password",
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
									on_click=lambda _: go_to_view(page=self.page, logger=logger, route="/sign_in")
								)
							),
							MainTitle(
								subtitle="Cambiar contraseña",
								top_margin=(SPACING * 2)
							),
							ft.Container(
								margin=ft.margin.only(top=SPACING),
								content=ft.Column(
									spacing=(SPACING * 1.5),
									controls=[
										self.cont_email,
										self.cont_password,
										self.cont_confirm_password
									]
								)
							),
							ft.Container(
								margin=ft.margin.only(top=(SPACING * 4)),
								content=ft.Column(
									controls=[
										self.btn_submit,
										ft.Divider(color=ft.colors.TRANSPARENT),
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
		# Case when only txt_email is displayed
		if not self.cont_password.visible and not self.cont_confirm_password.visible \
				and match(pattern=RGX_EMAIL, string=self.txt_email.value):
			self.btn_submit.disabled = False
		# Case all input fields are displayed
		elif self.cont_password.visible and self.cont_confirm_password.visible \
			and all([
				self.txt_password.value,
				self.txt_confirm_password.value,
				match(pattern=RGX_EMAIL, string=self.txt_email.value)]):
			self.btn_submit.disabled = False
		else:
			self.btn_submit.disabled = True

		self.page.update()

	def btn_back_clicked(self, _: ft.ControlEvent) -> None:
		self.cont_password.visible = False
		self.cont_confirm_password.visible = False
		self.page.update()

		go_to_view(page=self.page, logger=logger, route="/sign_in")

	def btn_submit_clicked(self, _: ft.ControlEvent) -> None:
		if self.cont_password.visible and self.cont_confirm_password.visible:
			logger.info("Changing password...")
		else:
			logger.info("Verifying email...")
			# self.btn_submit.disabled = True
			self.cont_password.visible = True
			self.cont_confirm_password.visible = True
			self.page.update()
