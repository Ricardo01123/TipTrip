from logging import getLogger
from requests import Response, post, delete
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Text, Stack, CircleAvatar, Image, ImageFit,
	ImageRepeat, ElevatedButton, IconButton, MainAxisAlignment, alignment,
	Offset, FontWeight, padding, margin, BoxShadow, border_radius, colors,
	ControlEvent, AlertDialog, TextButton, icons, TextStyle, Banner, ButtonStyle,
	Icon
)

from components.bars import *
from resources.config import *
from resources.functions import clean_basket, go_to_view
from resources.styles import btn_secondary_style, btn_danger_style


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class AccountView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.route = None

		self.btn_edit_data = None
		self.btn_delete_user = None

		self.dlg_confirm_delete_account: AlertDialog = AlertDialog(
			modal=True,
			title=Text("Eliminar cuenta"),
			content=Text(
				"¿Estás seguro de que deseas eliminar tu cuenta?\n"
				"Esta acción no se puede deshacer."
			),
			actions=[
				TextButton(
					"Cancelar",
					on_click=lambda _: self.page.close(self.dlg_confirm_delete_account)
				),
				TextButton("Aceptar", on_click=self.delete_account)
			],
			actions_alignment=MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_confirm_delete_account)
		)

		self.dlg_account_deleted: AlertDialog = AlertDialog(
			modal=True,
			title=Text("Cuenta eliminada"),
			content=Text("Su cuenta ha sido eliminada exitosamente."),
			actions=[
				TextButton("Aceptar", on_click=self.handle_ok_account_deleted)
			],
			actions_alignment=MainAxisAlignment.END,
			on_dismiss=self.handle_ok_account_deleted
		)

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
					on_click=self.bnr_handle_dismiss
				)
			],
			force_actions_below=True
		)

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.route = "/account"

		self.btn_edit_data: ElevatedButton = ElevatedButton(
			width=self.page.width,
			icon=icons.EDIT,
			text="Editar perfil",
			on_click=self.btn_edit_data_clicked,
			**btn_secondary_style
		)

		self.btn_delete_user: ElevatedButton = ElevatedButton(
			width=self.page.width,
			icon=icons.DELETE,
			text="Eliminar cuenta",
			on_click=self.btn_delete_user_clicked,
			**btn_danger_style
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
								content=Text(value=self.basket.get("username")[:2].upper()),
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
					padding=padding.only(
						top=(SPACING * 2),
						right=SPACING,
						bottom=SPACING,
						left=SPACING,
					),
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
						width=self.page.width,
						alignment=MainAxisAlignment.START,
						spacing=SPACING,
						controls=[
							Container(
								height=80,
								bgcolor=colors.WHITE,
								padding=padding.symmetric(
									vertical=(SPACING / 2),
									horizontal=SPACING
								),
								border_radius=border_radius.all(
									value=RADIUS
								),
								shadow=BoxShadow(
									blur_radius=LOW_BLUR,
									color=colors.GREY_500
								),
								content=Column(
									alignment=MainAxisAlignment.CENTER,
									spacing=0,
									controls=[
										Container(
											expand=1,
											width=self.page.width,
											alignment=alignment.bottom_left,
											content=Text(
												value=self.basket.get("username").capitalize(),
												color=colors.BLACK,
												weight=FontWeight.BOLD,
												size=20,
											),
										),
										Container(
											expand=1,
											width=self.page.width,
											alignment=alignment.top_left,
											content=Text(
												value="Nombre de usuario",
												color=colors.BLACK
											),
										)
									]
								)
							),
							Container(
								height=80,
								bgcolor=colors.WHITE,
								padding=padding.symmetric(
									vertical=(SPACING / 2),
									horizontal=SPACING
								),
								border_radius=border_radius.all(
									value=RADIUS
								),
								shadow=BoxShadow(
									blur_radius=LOW_BLUR,
									color=colors.GREY_500
								),
								content=Column(
									alignment=MainAxisAlignment.CENTER,
									spacing=0,
									controls=[
										Container(
											expand=1,
											width=self.page.width,
											alignment=alignment.bottom_left,
											content=Text(
												value=self.basket.get("created_at"),
												color=colors.BLACK,
												size=18,
											),
										),
										Container(
											expand=1,
											width=self.page.width,
											alignment=alignment.top_left,
											content=Text(
												value="Fecha de creación de la cuenta",
												color=colors.BLACK,
											),
										)
									]
								)
							),
							Container(
								margin=margin.only(top=SPACING),
								padding=padding.symmetric(horizontal=SPACING),
								alignment=alignment.center,
								content=self.btn_edit_data
							),
							Container(
								padding=padding.symmetric(horizontal=SPACING),
								alignment=alignment.center,
								content=self.btn_delete_user
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

	def bnr_handle_dismiss(self, event: ControlEvent) -> None:
		self.bnr_error.content = Text(value="")
		self.page.close(self.bnr_error)

	def btn_edit_data_clicked(self, event: ControlEvent) -> None:
		logger.info("Edit data button clicked")
		pass

	def btn_delete_user_clicked(self, event: ControlEvent) -> None:
		logger.info("Delete user button clicked")
		self.page.open(self.dlg_confirm_delete_account)

	def handle_ok_account_deleted(self, event: ControlEvent) -> None:
		self.page.close(self.dlg_account_deleted)
		clean_basket(self.basket, logger=logger)
		go_to_view(page=self.page, logger=logger, route="") # Redirect to sign in

	def delete_account(self, event: ControlEvent) -> None:
		logger.info("Making request to delete account...")
		response: Response = delete(
			url=f"{BACK_END_URL}/{DELETE_USER_ENDPOINT}",
			headers={
				"Content-Type": "application/json",
				"Authorization": f"Bearer {self.basket.get('session_token')}"
			},
			json={
				"email": self.basket.get("email"),
			}
		)

		print(response)
		print(response.status_code)

		if response.status_code == 200:
			logger.info("Account deleted successfully")
			self.page.open(self.dlg_account_deleted)

		else:
			logger.error("Error deleting account")
			self.page.close(self.dlg_confirm_delete_account)
			self.bnr_error.content = Text(
				value=(
					"Ocurrió un error al eliminar la cuenta. "
					"Favor de intentarlo de nuevo más tarde."
				),
				style=TextStyle(color=colors.RED)
			)
			self.page.open(self.bnr_error)
