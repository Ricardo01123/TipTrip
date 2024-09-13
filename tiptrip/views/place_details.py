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
													value=self.place_data["nombre"],
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
																	value=self.place_data["clasificacion_sitio"],
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
																	value=self.place_data["puntuacion"],
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
			return response.json()["data"]
		else:
			return Container(
					alignment=alignment.center,
					content=Text(
						value="No se encontró información del lugar.",
						color=colors.BLACK,
						size=35
					)
				)

	def fill_data_tabs(self) -> list:
		result: list = []

		if any([
			self.place_data["horario"],
			self.place_data["costos"],
			self.place_data["calle_numero"],
			self.place_data["colonia"],
			self.place_data["cp"],
			self.place_data["delegacion_municipio"],
			self.place_data["entidad_federativa"],
			self.place_data["referencias"],
		]):
			info: Column = Column()

			if self.place_data["horario"]:
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
										value=self.place_data["horario"],
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			if self.place_data["costos"]:
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
										value=self.place_data["costos"],
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			if any([
				self.place_data["calle_numero"],
				self.place_data["colonia"],
				self.place_data["cp"],
				self.place_data["delegacion_municipio"],
				self.place_data["entidad_federativa"],
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
											f"{self.place_data['calle_numero']}, "
											f"{self.place_data['colonia']}, "
											f"{self.place_data['cp']}, "
											f"{self.place_data['delegacion_municipio']}, "
											f"{self.place_data['entidad_federativa']}."
										),
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			if self.place_data["referencias"]:
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
										value=self.place_data["referencias"],
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

		if self.place_data["descripcion"]:
			result.append(
				Tab(
					text="Descripción",
					content=Container(
						content=Text(
							value=self.place_data["descripcion"],
							color=colors.BLACK
						)
					)
				)
			)

		if self.place_data["reseña_historica"]:
			result.append(
				Tab(
					text="Reseña histórica",
					content=Container(
						content=Text(
							value=self.place_data["reseña_historica"],
							color=colors.BLACK
						)
					)
				)
			)

		if self.place_data["reseña_general"]:
			result.append(
				Tab(
					text="Reseña general",
					content=Container(
						content=Text(
							value=self.place_data["reseña_general"],
							color=colors.BLACK
						)
					)
				)
			)

		if self.place_data["servicios"]:
			result.append(
				Tab(
					text="Servicios",
					content=Container(
						content=Text(
							value=self.place_data["servicios"],
							color=colors.BLACK
						)
					)
				)
			)

		if self.place_data["actividades"]:
			result.append(
				Tab(
					text="Actividades",
					content=Container(
						content=Text(
							value=self.place_data["actividades"],
							color=colors.BLACK
						)
					)
				)
			)

		if self.place_data["salas_permanentes"]:
			result.append(
				Tab(
					text="Salas permanentes",
					content=Container(
						content=Text(
							value=self.place_data["salas_permanentes"],
							color=colors.BLACK
						)
					)
				)
			)

		if self.place_data["salas_temporales"]:
			result.append(
				Tab(
					text="Salas temporales",
					content=Container(
						content=Text(
							value=self.place_data["salas_temporales"],
							color=colors.BLACK
						)
					)
				)
			)

		if any([
			self.place_data["email"],
			self.place_data["telefono"],
			self.place_data["pagina_web"],
			self.place_data["pagina_sic"]
		]):
			contact_info: Column = Column()

			if self.place_data["email"]:
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
										value=self.place_data["email"],
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			if self.place_data["telefono"]:
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
										value=self.place_data["telefono"],
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			if self.place_data["pagina_web"]:
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
										value=self.place_data["pagina_web"],
										color=colors.BLACK
									)
								)
							]
						)
					)
				)

			if self.place_data["pagina_sic"]:
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
										value=self.place_data["pagina_sic"],
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

	def get_items(self) -> list:
		items: list = []

		if self.place_data["ruta1"] is not None:
			items.append(self.place_data["ruta1"])

		if self.place_data["ruta2"] is not None:
			items.append(self.place_data["ruta2"])

		if self.place_data["ruta3"] is not None:
			items.append(self.place_data["ruta3"])

		if self.place_data["ruta4"] is not None:
			items.append(self.place_data["ruta4"])

		if self.place_data["ruta5"] is not None:
			items.append(self.place_data["ruta5"])

		return items

	# def get_items(self) -> list:
	# 	place_name = self.params.get("place_name")
	# 	dir: str = place_name.replace(' ', '_').replace(',', '_').lower()
	# 	path: str = join(ASSETS_ABSPATH, "places", dir)
	# 	images: list = listdir(path)
	# 	result = [join("places", dir, image) for image in images]
	# 	print(result)
	# 	return result
