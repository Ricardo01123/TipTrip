from logging import getLogger
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Text, ElevatedButton, IconButton,
	padding, margin, colors, icons
)

# from data import db
from resources.config import *
from resources.texts import TERMS_CONDITIONS
from components.titles import MainTitleColumn
from resources.functions import secondary_btn_hover, go_to_view
from resources.styles import cont_main_style, btn_secondary_style


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class TermsConditionsView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.btn_back: ElevatedButton = ElevatedButton(
			icon=icons.LOGIN,
			text="Regresar a Registrarse",
			on_hover=secondary_btn_hover,
			on_click=lambda _: go_to_view(
				page=self.page,
				logger=logger,
				route="sign_up"
			),
			**btn_secondary_style
		)

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		return View(
			route="/terms_conditions",
			padding=padding.all(value=0.0),
			bgcolor=MAIN_COLOR,
			controls=[
				Container(
					content=Column(
						controls=[
							IconButton(
								icon=icons.ARROW_BACK,
								icon_color=colors.BLACK,
								on_click=lambda _: go_to_view(
									page=self.page,
									logger=logger,
									route="sign_up"
								),
							),
							MainTitleColumn(
								subtitle="Términos y condiciones",
								top_margin=(SPACING / 2)
							),
							Container(
								margin=margin.only(top=SPACING),
								content=Column(
									controls=[
										Text(value=TERMS_CONDITIONS)
									]
								)
							),
							Container(
								margin=margin.only(top=SPACING),
								content=self.btn_back
							)
						]
					),
					**cont_main_style
				)
			]
		)
