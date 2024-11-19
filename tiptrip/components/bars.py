import flet as ft
from logging import Logger

from resources.config import *
from resources.functions import go_to_view


class TopBar(ft.AppBar):
	def __init__(self, page: ft.Page, leading: bool, logger: Logger) -> None:
		super().__init__(
			bgcolor=MAIN_COLOR,
			leading=(
				ft.IconButton(
					icon=ft.icons.ARROW_BACK,
					icon_color=ft.colors.BLACK,
					on_click=lambda _: go_to_view(page=page, logger=logger, route='/')
				)
				if leading == True
				else None
			),
			title=ft.Text(
				value=PROJECT_NAME,
				color=ft.colors.BLACK
			),
			actions=[
				ft.IconButton(
					icon=ft.icons.LOGOUT,
					icon_color=ft.colors.BLACK,
					padding=ft.padding.only(right=SPACING),
					tooltip="Cerrar sesión",
					on_click=lambda _: go_to_view(page=page, logger=logger, route="/sign_in")
				)
			]
		)


class BottomBar(ft.Container):
	def __init__(self, page: ft.Page, logger: Logger, current_route: str) -> None:
		super().__init__(
			# expand=True,
			width=page.width,
			height=60,
			bgcolor=ft.colors.WHITE,
			border_radius=ft.border_radius.only(top_left=RADIUS, top_right=RADIUS),
			shadow=ft.BoxShadow(
				blur_radius=(BLUR / 2),
				offset=ft.Offset(0, -2),
				color=ft.colors.GREY
			),
			content=ft.Row(
				alignment=ft.MainAxisAlignment.SPACE_EVENLY,
				controls=[
					ft.IconButton(
						icon=ft.icons.HOME,
						icon_color=(
							MAIN_COLOR
							if current_route == '/'
							else ft.colors.BLACK
						),
						icon_size=30,
						on_click=lambda _: go_to_view(page=page, logger=logger, route='/')
					),
					ft.IconButton(
						icon=ft.icons.SUPPORT_AGENT,
						icon_color=ft.colors.BLACK,
						icon_size=30,
						on_click=lambda _: go_to_view(page=page, logger=logger, route="/chatbot")
					),
					ft.IconButton(
						icon=ft.icons.BOOKMARK_BORDER,
						icon_color=(
							MAIN_COLOR
							if current_route == "/favorites"
							else ft.colors.BLACK
						),
						icon_size=30,
						on_click=lambda _: go_to_view(page=page, logger=logger, route="/favorites")
					),
					ft.IconButton(
						icon=ft.icons.ACCOUNT_CIRCLE,
						icon_color=(
							MAIN_COLOR
							if current_route == "/account"
							else ft.colors.BLACK
						),
						icon_size=30,
						on_click=lambda _: go_to_view(page=page, logger=logger, route="/account")
					)
				]
			)
		)
