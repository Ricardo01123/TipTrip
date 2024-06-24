from logging import Logger
from flet import (
	AppBar, Page, Container, Row, Text, IconButton, padding, border_radius,
	BoxShadow, colors, icons, Offset, MainAxisAlignment
)

from resources.config import *
from resources.functions import go_to_view


class TopBar(AppBar):
	def __init__(self, page: Page, leading: bool, logger: Logger) -> None:
		super().__init__(
			bgcolor=MAIN_COLOR,
			leading=(
				IconButton(
					icon=icons.ARROW_BACK,
					on_click=lambda _: go_to_view(
						page=page,
						logger=logger,
						route="home"
					)
				)
				if leading == True
				else None
			),
			title=Text(value=PROJECT_NAME),
			actions=[
				IconButton(
					icon=icons.LOGOUT,
					icon_color=colors.BLACK,
					padding=padding.only(right=SPACING),
					tooltip="Cerrar sesión",
					on_click=lambda _: go_to_view(
						page=page,
						logger=logger,
						route=""  # '/'
					)
				)
			]
		)


class BottomBar(Container):
	def __init__(self, page: Page, logger: Logger, current_route: str) -> None:
		super().__init__(
			expand=True,
			height=60,
			bgcolor=colors.WHITE,
			border_radius=border_radius.only(top_left=RADIUS, top_right=RADIUS),
			shadow=BoxShadow(blur_radius=(BLUR / 2), offset=Offset(0, -2), color=colors.GREY),
			content=Row(
				alignment=MainAxisAlignment.SPACE_EVENLY,
				controls=[
					IconButton(
						icon=icons.HOME,
						icon_color=(
							MAIN_COLOR
							if current_route == "/home"
							else colors.BLACK
						),
						icon_size=30,
						on_click=lambda _: go_to_view(
							page=page,
							logger=logger,
							route="home"
						)
					),
					IconButton(
						icon=icons.SUPPORT_AGENT,
						icon_color=colors.BLACK,
						icon_size=30,
						on_click=lambda _: go_to_view(
							page=page,
							logger=logger,
							route="chatbot"
						)
					),
					IconButton(
						icon=icons.ACCOUNT_CIRCLE,
						icon_color=(
							MAIN_COLOR
							if current_route == "/account"
							else colors.BLACK
						),
						icon_size=30,
						on_click=lambda _: go_to_view(
							page=page,
							logger=logger,
							route="account"
						)
					)
				]
			)
		)
