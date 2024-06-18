import logging
from flet_route import Params, Basket

from flet import (
	Page, View, AppBar, Container, Column, Row, Banner, Text, TextField, ElevatedButton, IconButton, Icon,
	CrossAxisAlignment, alignment, Markdown, padding, margin, BoxShadow, border_radius, colors, icons, ControlEvent
)

from data import db
from resources.config import *
from resources.functions import go_to_view


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


class HomeView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		return View(
			route="/home",
			padding=padding.all(value=0.0),
			controls=[
				AppBar(
					leading=IconButton(
						icon=icons.VERIFIED_USER,
					),
					title=Text(value=basket.get("username")),
					actions=[
						IconButton(
							icon=icons.LOGOUT,
							on_click=lambda _: go_to_view(page=self.page, logger=logger, route="")  # '/'
						)
					]
				),
			]
		)
