import logging
from flet_route import Params, Basket

from flet import (
	Page, View, Container, AppBar, Column, Row, Text, ListView,
	IconButton, ElevatedButton, DataTable, DataColumn, DataRow, DataCell,
	MainAxisAlignment, CrossAxisAlignment,
	ScrollMode, ControlEvent,
	padding, icons,
)

from data import db
from resources.functions import clean_basket
from components.history_table import HistoryTable

from resources.config import (
	TITLE_SIZE, TEXT_SIZE, PROJECT_NAME, PROJECT_NAME_SIZE,
	APP_WIDTH, EXTERIOR_PADDING, COMPONENTS_WIDTH
)


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


class HistoryView:
	def __init__(self):
		self.page = None
		self.params = None
		self.basket = None
		self.data_table = None
		self.list_view = None

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		return View(
			route="/history",
			scroll=ScrollMode.AUTO,
			vertical_alignment=MainAxisAlignment.CENTER,
			horizontal_alignment=CrossAxisAlignment.CENTER,
			controls=[
				AppBar(
					leading=IconButton(
						icon=icons.VERIFIED_USER,
					),
					title=Text(value=basket.get("username")),
					actions=[
						IconButton(
							icon=icons.LOGOUT,
							on_click=self.sign_out
						)
					]
				),
				Container(
					# width=APP_WIDTH,
					padding=padding.only(
						left=EXTERIOR_PADDING,
						right=EXTERIOR_PADDING
					),
					content=Column(
						alignment=MainAxisAlignment.START,
						spacing=30,
						controls=[
							Container(
								content=Text(
									value=PROJECT_NAME,
									size=PROJECT_NAME_SIZE
								)
							),
							Container(
								content=Text(
									value="Historial de pedidos",
									size=TITLE_SIZE
								)
							),
							Container(
								content=Row(
									scroll=ScrollMode.ALWAYS,
									controls=[HistoryTable()]
								)
							),
							Container(
								padding=padding.only(bottom=EXTERIOR_PADDING),
								content=ElevatedButton(
									text="Regresar",
									width=COMPONENTS_WIDTH,
									on_click=lambda _: self.page.go(
										f"/home/{self.basket.get('username')}")
								)
							)
						]
					)
				)
			]
		)

	def sign_out(self, event: ControlEvent):
		logging.info("Cerrando sesión...")
		self.page.banner.close_banner(event)
		clean_basket(self.basket)
		self.page.go('/')
