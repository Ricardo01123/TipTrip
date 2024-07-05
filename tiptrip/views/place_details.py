from logging import getLogger
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Row, Text, Icon, MainAxisAlignment,
	alignment, Offset, ScrollMode, FontWeight, padding, BoxShadow,
	border_radius, colors, icons,
)

# from data import db
from components.bars import *
from resources.config import *
from components.carousel import Carousel


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class PlaceDetailsView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.route = None
		self.place_name = None

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.route = "/place_details/:place_name"
		self.place_name = self.params.get("place_name")

		return View(
			route=self.route,
			bgcolor=colors.WHITE,
			padding=padding.all(value=0.0),
			spacing=0,
			controls=[
				TopBar(page=self.page, leading=True, logger=logger),
				Container(
					width=self.page.width,
					height=RADIUS,
					bgcolor=MAIN_COLOR,
					border_radius=border_radius.only(
						bottom_left=RADIUS,
						bottom_right=RADIUS
					),
					shadow=BoxShadow(
						blur_radius=BLUR,
						color=colors.GREY_800
					),
				),
				Container(
					width=self.page.width,
					alignment=alignment.center,
					padding=padding.only(
						top=(SPACING / 2),
						right=SPACING,
						bottom=10,
						left=SPACING
					),
					content=Container(
						height=90,
						bgcolor=colors.WHITE,
						padding=padding.symmetric(
							vertical=(SPACING / 2),
							horizontal=SPACING
						),
						border_radius=border_radius.all(value=RADIUS),
						shadow=BoxShadow(
							blur_radius=LOW_BLUR,
							color=colors.GREY_500
						),
						content=Column(
							alignment=MainAxisAlignment.CENTER,
							spacing=10,
							controls=[
								Container(
									expand=1,
									width=self.page.width,
									alignment=alignment.bottom_left,
									content=Text(
										value=self.place_name.upper().replace('_', ' '),
										color=MAIN_COLOR,
										weight=FontWeight.BOLD,
										size=25,
									),
								),
								Container(
									expand=1,
									width=self.page.width,
									content=Row(
										spacing=0,
										alignment=MainAxisAlignment.SPACE_BETWEEN,
										controls=[
											Container(
												content=Row(
													spacing=10,
													controls=[
														Container(
															content=Icon(
																name=icons.MUSEUM_SHARP,
																color=SECONDARY_COLOR,
																size=18
															)
														),
														Container(
															content=Text(
																value="MUSEO",
																color=SECONDARY_COLOR,
																size=18
															)
														)
													]
												)
											),
											Container(
												width=70,
												bgcolor=SECONDARY_COLOR,
												border_radius=border_radius.all(
													value=15
												),
												content=Row(
													spacing=10,
													alignment=MainAxisAlignment.CENTER,
													controls=[
														Container(
															expand=1,
															alignment=alignment.center_right,
															content=Icon(
																name=icons.STAR_BORDER,
																color=colors.WHITE,
																size=18
															)
														),
														Container(
															expand=1,
															alignment=alignment.center_left,
															content=Text(
																value="5",
																color=colors.WHITE,
																size=18
															)
														)
													]
												)
											)
										]
									)
								)
							]
						)
					)
				),
				Container(
					width=self.page.width,
					padding=padding.only(
						right=10,
						left=10,
						bottom=10,
					),
					alignment=alignment.center,
					content=Carousel(
						page=self.page,
						items=[
							"bellas_artes.jpg",
							"castillo.jpg",
							"monumento.jpg"
						]
					)
				),
				Container(
					width=self.page.width,
					bgcolor=colors.WHITE,
					padding=padding.all(value=SPACING),
					border_radius=border_radius.only(
						top_left=RADIUS,
						top_right=RADIUS
					),
					shadow=BoxShadow(
						blur_radius=LOW_BLUR,
						offset=Offset(0, -2),
						color=colors.BLACK
					),
					content=Row(
						spacing=(SPACING / 2),
						scroll=ScrollMode.HIDDEN,
						controls=[
							Container(
								content=Text(
									value="Información general",
									color=MAIN_COLOR,
								),
								on_click=lambda _: print("Clicked!")
							),
							Container(
								content=Text(
									value="Descripción",
									color=colors.BLACK,
								)
							),
							Container(
								content=Text(
									value="Servicios",
									color=colors.BLACK,
								)
							),
							Container(
								content=Text(
									value="Salas permanentes",
									color=colors.BLACK,
								)
							)
						]
					)
				),
				Container(
					expand=1,
					width=self.page.width,
					bgcolor=colors.WHITE,
					padding=padding.only(
						left=SPACING,
						right=SPACING,
						bottom=(SPACING / 2),
					),
					content=Column(
						width=self.page.width,
						scroll=ScrollMode.HIDDEN,
						controls=[
							Text(
								value="Av. Paseo de la Reforma esq. Calz. Gandhi s/n, Col. Chapultepec Polanco, 11560, Miguel Hidalgo, Ciudad de México",
								color=colors.BLACK
							),
							Text(
								value="Av. Paseo de la Reforma esq. Calz. Gandhi s/n, Col. Chapultepec Polanco, 11560, Miguel Hidalgo, Ciudad de México",
								color=colors.BLACK
							),
							Text(
								value="Av. Paseo de la Reforma esq. Calz. Gandhi s/n, Col. Chapultepec Polanco, 11560, Miguel Hidalgo, Ciudad de México",
								color=colors.BLACK
							),
							Text(
								value="Av. Paseo de la Reforma esq. Calz. Gandhi s/n, Col. Chapultepec Polanco, 11560, Miguel Hidalgo, Ciudad de México",
								color=colors.BLACK
							),
							Text(
								value="Av. Paseo de la Reforma esq. Calz. Gandhi s/n, Col. Chapultepec Polanco, 11560, Miguel Hidalgo, Ciudad de México",
								color=colors.BLACK
							),
							Text(
								value="Av. Paseo de la Reforma esq. Calz. Gandhi s/n, Col. Chapultepec Polanco, 11560, Miguel Hidalgo, Ciudad de México",
								color=colors.BLACK
							),
							Text(
								value="Av. Paseo de la Reforma esq. Calz. Gandhi s/n, Col. Chapultepec Polanco, 11560, Miguel Hidalgo, Ciudad de México",
								color=colors.BLACK
							),
							Text(
								value="Av. Paseo de la Reforma esq. Calz. Gandhi s/n, Col. Chapultepec Polanco, 11560, Miguel Hidalgo, Ciudad de México",
								color=colors.BLACK
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
