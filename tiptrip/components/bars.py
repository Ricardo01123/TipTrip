import flet as ft
from logging import Logger

from resources.config import *
from resources.functions import go_to_view


class TopBar(ft.AppBar):
	def __init__(self, page: ft.Page, leading: bool, logger: Logger) -> None:
		self.page = page
		self.logger = logger

		super().__init__(
			bgcolor=MAIN_COLOR,
			leading=(
				ft.IconButton(
					icon=ft.Icons.ARROW_BACK,
					icon_color=ft.Colors.BLACK,
					on_click=lambda _: go_to_view(page=self.page, logger=self.logger, route='/')
				)
				if leading == True
				else None
			),
			title=ft.Text(
				value=PROJECT_NAME,
				color=ft.Colors.BLACK
			),
			actions=[
				ft.IconButton(
					icon=ft.Icons.LOGOUT,
					icon_color=ft.Colors.BLACK,
					padding=ft.padding.only(right=SPACING),
					tooltip="Cerrar sesión",
					on_click=self.logout
				)
			]
		)

	def logout(self, _: ft.ControlEvent) -> None:
		self.logger.info("Cleaning session...")
		self.page.session.clear()

		go_to_view(page=self.page, logger=self.logger, route="/sign_in")


class BottomBar(ft.BottomAppBar):
	def __init__(self, page: ft.Page, logger: Logger, current_route: str) -> None:
		super().__init__(
			bgcolor=MAIN_COLOR,
			shape=ft.NotchShape.CIRCULAR,
			elevation=0,
			content=ft.Row(
				alignment=ft.MainAxisAlignment.SPACE_EVENLY,
				controls=[
					ft.IconButton(
						icon=ft.Icons.HOME,
						icon_color=(
							ft.Colors.WHITE
							if current_route == '/'
							else ft.Colors.BLACK
						),
						icon_size=30,
						on_click=lambda _: go_to_view(page=page, logger=logger, route='/')
					),
					ft.IconButton(
						icon=ft.Icons.SUPPORT_AGENT,
						icon_color=ft.Colors.BLACK,
						icon_size=30,
						on_click=lambda _: go_to_view(page=page, logger=logger, route="/chatbot")
					),
					ft.IconButton(
						icon=ft.Icons.BOOKMARKS,
						icon_color=(
							ft.Colors.WHITE
							if current_route == "/favorites"
							else ft.Colors.BLACK
						),
						icon_size=30,
						on_click=lambda _: go_to_view(page=page, logger=logger, route="/favorites")
					),
					ft.IconButton(
						icon=ft.Icons.ACCOUNT_CIRCLE,
						icon_color=(
							ft.Colors.WHITE
							if current_route == "/account"
							else ft.Colors.BLACK
						),
						icon_size=30,
						on_click=lambda _: go_to_view(page=page, logger=logger, route="/account")
					)
				]
			)
		)
