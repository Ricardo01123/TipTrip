import logging
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Text, ElevatedButton, IconButton, Icon,
	alignment, padding, margin, BoxShadow, border_radius, colors, icons, ControlEvent
)

from data import db
from resources.config import *
from resources.texts import PRIVACY_POLITICS
from resources.functions import secondary_btn_hover, go_to_view


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


class PrivacyPoliticsView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.btn_back: ElevatedButton = ElevatedButton(
			icon=icons.LOGIN,
			text="Regresar a Iniciar sesión",
			color=MAIN_COLOR,
			width=(TOTAL_WIDTH - (MARGIN * 4)),
			on_hover=secondary_btn_hover,
			on_click=lambda _: go_to_view(page=self.page, logger=logger, route=""),  # '/'
		)

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		return View(
			route="/privacy_politics",
			padding=padding.all(value=0.0),
			bgcolor=MAIN_COLOR,
			controls=[
				Container(
					width=TOTAL_WIDTH,
					height=(HEIGHT_WITHOUT_HEADER - (MARGIN * 2)),
					margin=margin.all(value=MARGIN),
					padding=padding.all(value=PADDING),
					border_radius=border_radius.all(value=RADIUS),
					bgcolor=colors.WHITE,
					shadow=BoxShadow(blur_radius=BLUR),
					content=Column(
						controls=[
							IconButton(
								icon=icons.ARROW_BACK,
								icon_color=colors.BLACK,
								on_click=lambda _: go_to_view(page=self.page, logger=logger, route=""),  # '/'
							),
							Column(
								controls=[
									Container(
										alignment=alignment.center,
										content=Text(value=PROJECT_NAME, size=TITLE_SIZE),
									),
									Container(
										alignment=alignment.center,
										content=Text(value="Política de Privacidad", size=TEXT_SIZE)
									)
								]
							),
							Container(
								margin=margin.only(top=(MARGIN * 3)),
								content=Column(
									controls=[
										Text(value=PRIVACY_POLITICS)
									]
								)
							),
							Container(
								margin=margin.only(top=(MARGIN * 2)),
								content=self.btn_back
							)
						]
					)
				)
			]
		)
