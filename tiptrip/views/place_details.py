from logging import getLogger, info
from flet_route import Params, Basket

from flet import (
	Page, View, AppBar, BottomAppBar, Container, Stack, Column, Row, Text, TextField, TextButton, IconButton, Icon,
	Image, ImageFit, ImageRepeat,
	MainAxisAlignment, CrossAxisAlignment, alignment, VerticalAlignment, Offset, ScrollMode, FontWeight, ButtonStyle,
	padding, margin, BoxShadow, border_radius, colors, icons,
)

from data import db
from components.bars import *
from resources.config import *
from resources.functions import go_to_view
from components.place_details import PlaceHeader


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
			controls=[
				TopBar(page=self.page, leading=True, logger=logger),
				Container(
					expand=True,
					width=APP_WIDTH,
					content=Stack(
						controls=[
							Container(
								left=0,
								top=0,
								width=(APP_WIDTH - 16),
								height=185,
								bgcolor=MAIN_COLOR,
								content=Text(value=""),
							),
							Container(
								left=0,
								top=185 - RADIUS,
								bgcolor=colors.WHITE,
								width=(APP_WIDTH - 16),
								height=514,
								border_radius=border_radius.all(value=RADIUS),
								shadow=BoxShadow(
									blur_radius=BLUR,
									offset=Offset(0, -2),
									# color=colors.BLACK
								),
								content=Text(value="")
							),
							Container(
								left=0,
								top=10,
								width=(APP_WIDTH - 16),
								alignment=alignment.center,
								content=PlaceHeader(place_name=self.place_name),
							),
							Container(
								left=0,
								top=230,
								width=(APP_WIDTH - 16),
								alignment=alignment.center,
								content=Container(
									width=(APP_WIDTH - (SPACING * 2)),
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
								)
							),
							Container(
								top=260,
								width=(APP_WIDTH - 16),
								height=320,
								alignment=alignment.top_center,
								content=Column(
									width=(APP_WIDTH - (SPACING * 2)),
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
							Container(
								left=0,
								bottom=0,
								width=(APP_WIDTH - 16),
								content=BottomBar(
									page=self.page,
									logger=logger,
									current_route=self.route
								)
							)
						]
					)
				)
			]
		)