from os import listdir
from os.path import join
from requests import get, Response

from logging import getLogger
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Row, Tabs, Tab, Text, Icon,
	MainAxisAlignment, alignment, Offset, ScrollMode, FontWeight, padding,
	BoxShadow, border_radius, colors, icons,
)

from components.bars import *
from resources.config import *
from components.carousel import Carousel
from resources.functions import format_place_name


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class PlaceDetailsView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.route = None
		self.place_name = None
		self.place_data = None
		self.data_tabs = None

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.route: str = "/place_details/:place_name"
		self.place_data: dict | Container = self.get_place_data(self.params.get("place_name"))
		self.data_tabs: Tabs = Tabs(
			selected_index=0,
			animation_duration=300,
			divider_color=colors.TRANSPARENT,
			indicator_color=colors.TRANSPARENT,
			label_color=MAIN_COLOR,
			unselected_label_color=colors.BLACK,
			tabs=self.fill_data_tabs()
		)

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
						content=(
							self.place_data
							if isinstance(self.place_data, Container)
							else Column(
								alignment=MainAxisAlignment.CENTER,
								spacing=10,
								controls=[
									Container(
										width=self.page.width,
										alignment=alignment.bottom_left,
										content=Row(
											scroll=ScrollMode.HIDDEN,
											controls=[
												Text(
													value=self.place_data["name"],
													color=MAIN_COLOR,
													weight=FontWeight.BOLD,
													size=25,
												)
											]
										)
									),
									Container(
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
																	value=self.place_data["classification"],
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
													padding=padding.only(
														right=5
													),
													content=Row(
														spacing=5,
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
																	value=self.place_data["punctuation"],
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
						items=self.get_items()
					)
				),
				Container(
					expand=True,
					bgcolor=colors.WHITE,
					padding=padding.symmetric(
						vertical=(SPACING / 2),
						horizontal=SPACING,
					),
					border_radius=border_radius.only(
						top_left=RADIUS,
						top_right=RADIUS
					),
					shadow=BoxShadow(
						blur_radius=LOW_BLUR,
						offset=Offset(0, -2),
						color=colors.BLACK
					),
					content=Column(
						expand=True,
						scroll=ScrollMode.HIDDEN,
						controls=[self.data_tabs]
					)
				),
				BottomBar(
					page=self.page,
					logger=logger,
					current_route=self.route
				)
			]
		)

	def get_place_data(self, name: str) -> dict | Container:
		response: Response = get(
			url=f"{BACK_END_URL}/{GET_RECORD_ENDPOINT}",
			headers={
				"Content-Type": "application/json",
				"Authorization": f"Bearer {self.basket.get('session_token')}"
			},
			json={"place_name": name}
		)

		if response.status_code == 200:
			logger.debug(f"Response 200 OK: {response.json()}")
			return response.json()["data"]

		elif response.status_code == 204:
			logger.debug(f"Response 204 No Content: {response.json()}")
			return Container(
				alignment=alignment.center,
				content=Text(
					value="No se encontró información del sitio turístico seleccionado.",
					color=colors.BLACK,
					size=30
				)
			)

		else:
			logger.error(f"Response {response.status_code}: {response.json()}")
			return Container(
				alignment=alignment.center,
				content=Text(
					value=(
						"Ocurrió un error al obtener información del sitio "
						"turístico seleccionado.\n"
						"Favor de intentarlo de nuevo más tarde."
					),
					color=colors.BLACK,
					size=35
				)
			)

	def fill_data_tabs(self) -> list:
		result: list = []

		if any([
			self.place_data["schedules"],
			self.place_data["prices"],
			self.place_data["street_number"],
			self.place_data["colony"],
			self.place_data["cp"],
			self.place_data["municipality"],
			self.place_data["state"],
			self.place_data["how_to_arrive"],
		]):
			info: Column = Column()

			if self.place_data["schedules"]:
				info.controls.append(
					Container(
						content=Column(
							controls=[
								Container(
									content=Text(
										value=f"\nHorarios:",
										weight=FontWeight.BOLD,
										color=colors.BLACK
									)
								),
								Container(
									content=Text(
										value=self.place_data["schedules"],
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			if self.place_data["prices"]:
				info.controls.append(
					Container(
						content=Column(
							controls=[
								Container(
									content=Text(
										value=f"\nCostos:",
										weight=FontWeight.BOLD,
										color=colors.BLACK
									)
								),
								Container(
									content=Text(
										value=self.place_data["prices"],
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			if any([
				self.place_data["street_number"],
				self.place_data["colony"],
				self.place_data["cp"],
				self.place_data["municipality"],
				self.place_data["state"],
			]):
				info.controls.append(
					Container(
						content=Column(
							controls=[
								Container(
									content=Text(
										value=f"\nDirección:",
										weight=FontWeight.BOLD,
										color=colors.BLACK
									)
								),
								Container(
									content=Text(
										value=(
											f"{self.place_data['street_number']}, "
											f"{self.place_data['colony']}, "
											f"{self.place_data['cp']}, "
											f"{self.place_data['municipality']}, "
											f"{self.place_data['state']}."
										),
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			if self.place_data["how_to_arrive"]:
				info.controls.append(
					Container(
						content=Column(
							controls=[
								Container(
									content=Text(
										value=f"\nReferencias para llegar:",
										weight=FontWeight.BOLD,
										color=colors.BLACK
									)
								),
								Container(
									content=Text(
										value=self.place_data["how_to_arrive"],
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			result.append(
				Tab(
					text="Información",
					content=info
				)
			)

		if self.place_data["description"]:
			result.append(
				Tab(
					text="Descripción",
					content=Container(
						content=Text(
							value=self.place_data["description"],
							color=colors.BLACK
						)
					)
				)
			)

		if self.place_data["historic_review"]:
			result.append(
				Tab(
					text="Reseña histórica",
					content=Container(
						content=Text(
							value=self.place_data["historic_review"],
							color=colors.BLACK
						)
					)
				)
			)

		if self.place_data["review"]:
			result.append(
				Tab(
					text="Reseña general",
					content=Container(
						content=Text(
							value=self.place_data["review"],
							color=colors.BLACK
						)
					)
				)
			)

		if self.place_data["services"]:
			result.append(
				Tab(
					text="Servicios",
					content=Container(
						content=Text(
							value=self.place_data["services"],
							color=colors.BLACK
						)
					)
				)
			)

		if self.place_data["activities"]:
			result.append(
				Tab(
					text="Actividades",
					content=Container(
						content=Text(
							value=self.place_data["activities"],
							color=colors.BLACK
						)
					)
				)
			)

		if self.place_data["permanent_exhibitions"]:
			result.append(
				Tab(
					text="Salas permanentes",
					content=Container(
						content=Text(
							value=self.place_data["permanent_exhibitions"],
							color=colors.BLACK
						)
					)
				)
			)

		if self.place_data["temporal_exhibitions"]:
			result.append(
				Tab(
					text="Salas temporales",
					content=Container(
						content=Text(
							value=self.place_data["temporal_exhibitions"],
							color=colors.BLACK
						)
					)
				)
			)

		if any([
			self.place_data["mail"],
			self.place_data["phone"],
			self.place_data["website"],
			self.place_data["sic_website"]
		]):
			contact_info: Column = Column()

			if self.place_data["mail"]:
				contact_info.controls.append(
					Container(
						content=Column(
							controls=[
								Container(
									content=Text(
										value=f"\nCorreo electrónico:",
										weight=FontWeight.BOLD,
										color=colors.BLACK
									)
								),
								Container(
									content=Text(
										value=self.place_data["mail"],
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			if self.place_data["phone"]:
				contact_info.controls.append(
					Container(
						content=Column(
							controls=[
								Container(
									content=Text(
										value=f"\nTeléfono:",
										weight=FontWeight.BOLD,
										color=colors.BLACK
									)
								),
								Container(
									content=Text(
										value=self.place_data["phone"],
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			if self.place_data["website"]:
				contact_info.controls.append(
					Container(
						content=Column(
							controls=[
								Container(
									content=Text(
										value=f"\nPágina web:",
										weight=FontWeight.BOLD,
										color=colors.BLACK
									)
								),
								Container(
									content=Text(
										value=self.place_data["website"],
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			if self.place_data["sic_website"]:
				contact_info.controls.append(
					Container(
						content=Column(
							controls=[
								Container(
									content=Text(
										value=f"\nPágina del gobierno (SIC):",
										weight=FontWeight.BOLD,
										color=colors.BLACK
									)
								),
								Container(
									content=Text(
										value=self.place_data["sic_website"],
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			result.append(
				Tab(
					text="Contacto",
					content=contact_info
				)
			)

		if result == []:
			result.append(
				Tab(
					text="Error",
					content=Container(
						content=Text(
							value="No se encontró información",
							color=colors.BLACK
						)
					)
				)
			)

		return result

	# def get_items(self) -> list:
	# 	items: list = []

	# 	if self.place_data["ruta1"] is not None:
	# 		items.append(self.place_data["ruta1"])

	# 	if self.place_data["ruta2"] is not None:
	# 		items.append(self.place_data["ruta2"])

	# 	if self.place_data["ruta3"] is not None:
	# 		items.append(self.place_data["ruta3"])

	# 	if self.place_data["ruta4"] is not None:
	# 		items.append(self.place_data["ruta4"])

	# 	if self.place_data["ruta5"] is not None:
	# 		items.append(self.place_data["ruta5"])

	# 	return items

	def get_items(self) -> list:
		dir: str = format_place_name(self.params.get("place_name"))
		path: str = join(ASSETS_ABSPATH, "places", dir)
		images: list = listdir(path)
		if images:
			return [join("places", dir, image) for image in images]
		else:
			return ["/default.png"]
