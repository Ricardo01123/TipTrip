from logging import getLogger
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Text, ElevatedButton, IconButton,
	padding, margin, colors, icons
)

# from data import db
from resources.config import *
from components.titles import MainTitle
from resources.functions import go_to_view
from resources.texts import TERMS_CONDITIONS
from resources.styles import cont_main_style, btn_secondary_style


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class TermsConditionsView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None
		self.btn_back = None

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.btn_back: ElevatedButton = ElevatedButton(
			width=self.page.width,
			content=Text(
				value="Regresar a Registrarse",
				size=BTN_TEXT_SIZE
			),
			on_click=lambda _: go_to_view(
				page=self.page,
				logger=logger,
				route="sign_up"
			),
			**btn_secondary_style
		)

		return View(
			route="/terms_conditions",
			padding=padding.all(value=0.0),
			bgcolor=MAIN_COLOR,
			controls=[
				Container(
					content=Column(
						controls=[
							Container(
								content=IconButton(
									icon=icons.ARROW_BACK,
									icon_color=colors.BLACK,
									on_click=lambda _: go_to_view(
										page=self.page,
										logger=logger,
										route="sign_up"
									),
								)
							),
							MainTitle(
								subtitle="Términos y condiciones",
								top_margin=(SPACING / 2)
							),
							Container(
								margin=margin.only(top=SPACING),
								content=Column(
									controls=[
										Text(
											value=TERMS_CONDITIONS,
											color=colors.BLACK
										)
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
