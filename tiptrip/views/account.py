import flet as ft
from os import listdir
from os.path import join
from requests import delete, Response
from logging import Logger, getLogger


from components.bars import *
from resources.config import *
from resources.functions import go_to_view, get_user_image
from resources.styles import btn_secondary_style, btn_danger_style


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class AccountView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page
		self.user_image: str = get_user_image()

		# Custom components
		self.dlg_confirm_delete_account: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Eliminar cuenta"),
			content=ft.Text(
				"¿Estás seguro de que deseas eliminar tu cuenta?\n"
				"Esta acción no se puede deshacer."
			),
			actions=[
				ft.TextButton(
					text="Cancelar",
					on_click=lambda _: self.page.close(self.dlg_confirm_delete_account)
				),
				ft.TextButton(
					text="Aceptar",
					on_click=self.delete_account
				)
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_confirm_delete_account)
		)
		self.dlg_account_deleted: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Cuenta eliminada"),
			content=ft.Text("Su cuenta ha sido eliminada exitosamente."),
			actions=[
				ft.TextButton("Aceptar", on_click=self.handle_ok_account_deleted)
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=self.handle_ok_account_deleted
		)
		self.dlg_error: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Error al eliminar cuenta"),
			content=ft.Text(
				value=(
					"Ocurrió un error al eliminar la cuenta. "
					"Favor de intentarlo de nuevo más tarde."
				)
			),
			actions=[
				ft.TextButton(
					text="Aceptar",
					on_click=lambda _: self.page.close(self.dlg_error)
				),
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_error)
		)
		self.btn_delete_user: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			icon=ft.Icons.DELETE,
			text="Eliminar cuenta",
			on_click=lambda _: self.page.open(self.dlg_confirm_delete_account),
			**btn_danger_style
		)

		# View native attributes
		super().__init__(
			route="/account",
			bgcolor=MAIN_COLOR,
			padding=ft.padding.all(value=0.0),
			spacing=0,
			controls=[
				TopBar(page=self.page, leading=True, logger=logger),
				ft.Container(
					width=self.page.width,
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
								size=300,
							)
						)
					)
				),
				ft.Container(
					expand=True,
					width=self.page.width,
					bgcolor=ft.Colors.WHITE,
					padding=ft.padding.only(
						top=(SPACING * 2),
						right=SPACING,
						bottom=SPACING,
						left=SPACING,
					),
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
						width=self.page.width,
						alignment=ft.MainAxisAlignment.START,
						spacing=SPACING,
						scroll=ft.ScrollMode.HIDDEN,
						controls=[
							ft.Container(
								height=80,
								bgcolor=ft.Colors.WHITE,
								padding=ft.padding.symmetric(
									vertical=(SPACING / 2),
									horizontal=SPACING
								),
								border_radius=ft.border_radius.all(
									value=RADIUS
								),
								shadow=ft.BoxShadow(
									blur_radius=LOW_BLUR,
									color=ft.Colors.GREY_500
								),
								content=ft.Column(
									alignment=ft.MainAxisAlignment.CENTER,
									spacing=0,
									controls=[
										ft.Container(
											expand=1,
											width=self.page.width,
											alignment=ft.alignment.bottom_left,
											content=ft.Text(
												value=self.page.session.get("username"),
												color=ft.Colors.BLACK,
												weight=ft.FontWeight.BOLD,
												size=20,
											),
										),
										ft.Container(
											expand=1,
											width=self.page.width,
											alignment=ft.alignment.top_left,
											content=ft.Text(
												value="Nombre de usuario",
												color=ft.Colors.BLACK
											),
										)
									]
								)
							),
							ft.Container(
								height=80,
								bgcolor=ft.Colors.WHITE,
								padding=ft.padding.symmetric(
									vertical=(SPACING / 2),
									horizontal=SPACING
								),
								border_radius=ft.border_radius.all(
									value=RADIUS
								),
								shadow=ft.BoxShadow(
									blur_radius=LOW_BLUR,
									color=ft.Colors.GREY_500
								),
								content=ft.Column(
									alignment=ft.MainAxisAlignment.CENTER,
									spacing=0,
									controls=[
										ft.Container(
											expand=1,
											width=self.page.width,
											alignment=ft.alignment.bottom_left,
											content=ft.Text(
												value=self.page.session.get("created_at"),
												color=ft.Colors.BLACK,
												size=18,
											),
										),
										ft.Container(
											expand=1,
											width=self.page.width,
											alignment=ft.alignment.top_left,
											content=ft.Text(
												value="Fecha de creación de la cuenta",
												color=ft.Colors.BLACK,
											),
										)
									]
								)
							),
							ft.Container(
								margin=ft.margin.only(top=SPACING),
								padding=ft.padding.symmetric(horizontal=SPACING),
								alignment=ft.alignment.center,
								content=ft.ElevatedButton(
									width=self.page.width,
									icon=ft.Icons.EDIT,
									text="Editar perfil",
									on_click=self.go_to_update_user,
									**btn_secondary_style
								)
							),
							ft.Container(
								padding=ft.padding.symmetric(horizontal=SPACING),
								alignment=ft.alignment.center,
								content=self.btn_delete_user
							)
						]
					)
				)
			],
			bottom_appbar=BottomBar(page=self.page, logger=logger, current_route="/account")
		)

	def go_to_update_user(self, _: ft.ControlEvent) -> None:
		go_to_view(page=self.page, logger=logger, route="/update_user")

	def handle_ok_account_deleted(self, _: ft.ControlEvent) -> None:
		self.page.close(self.dlg_account_deleted)
		go_to_view(page=self.page, logger=logger, route="/sign_in")

	def delete_account(self, _: ft.ControlEvent) -> None:
		self.page.close(self.dlg_confirm_delete_account)

		logger.info("Making request to delete account...")
		response: Response = delete(
			url=f"{BACK_END_URL}/{USERS_ENDPOINT}/{self.page.session.get('id')}",
			headers={
				"Content-Type": "application/json",
				"Authorization": f"Bearer {self.page.session.get('session_token')}"
			}
		)

		if response.status_code == 200:
			logger.info("Account deleted successfully")
			self.page.open(self.dlg_account_deleted)

		else:
			logger.error("Error deleting account")
			self.page.open(self.dlg_error)
