from flet import *
from os import listdir
from os.path import join
from logging import getLogger
from requests import get, Response
from flet_route import Params, Basket

from components.bars import *
from resources.config import *
from resources.functions import *
from components.place_card import PlaceCard
from resources.styles import txt_messages_style


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class HomeView:
	def __init__(self) -> None:
		self.route = "/home"

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.txt_place_searcher: TextField = TextField(
			prefix_icon=icons.SEARCH,
			hint_text="Busca un lugar",
			on_change=self.search_place,
			**txt_messages_style
		)

		# Filters variables
		self.drd_municipality: Dropdown = Dropdown(
			label="Filtrar por delegación",
			options=[
				dropdown.Option("Álvaro Obregón"),
				dropdown.Option("Azcapotzalco"),
				dropdown.Option("Benito Juárez"),
				dropdown.Option("Coyoacán"),
				dropdown.Option("Cuajimalpa de Morelos"),
				dropdown.Option("Cuauhtémoc"),
				dropdown.Option("Gustavo A. Madero"),
				dropdown.Option("Iztacalco"),
				dropdown.Option("Iztapalapa"),
				dropdown.Option("La Magdalena Contreras"),
				dropdown.Option("Miguel Hidalgo"),
				dropdown.Option("Milpa Alta"),
				dropdown.Option("San Ángel"),
				dropdown.Option("Tláhuac"),
				dropdown.Option("Tlalpan"),
				dropdown.Option("Venustiano Carranza"),
				dropdown.Option("Xochimilco")
			]
		)

		self.drd_categories: Dropdown = Dropdown(
			label="Filtrar por categoría",
			options=[
				dropdown.Option("Arquitectura"),
				dropdown.Option("Centro cultural"),
				dropdown.Option("Centro religioso"),
				dropdown.Option("Escultura"),
				dropdown.Option("Experiencia"),
				dropdown.Option("Monumento"),
				dropdown.Option("Mural"),
				dropdown.Option("Museo"),
				dropdown.Option("Zona arqueológica")
			]
		)

		self.sld_distance: Slider = Slider(
			min=1,
			max=15,
			divisions=5,
			label="{value} km",
			disabled=True
		)

		self.chk_distance: Checkbox = Checkbox(
			label="Filtrar por cercanía",
			value=False,
			on_change=self.hide_show_slider
		)

		self.dlg_sites_filter: AlertDialog = AlertDialog(
			modal=True,
			adaptive=True,
			title=Text("Filtrar sitios turísticos"),
			content=Column(
				controls=[
					Container(content=self.drd_categories),
					Container(content=self.drd_municipality),
					Container(content=self.chk_distance),
					Container(content=self.sld_distance),
					Container(
						content=TextButton(
							text="Eliminar filtros",
							on_click=self.clean_filters
						),
					)
				]
			),
			actions=[
				TextButton(
					text="Cancelar",
					on_click=lambda _: self.page.close(self.dlg_sites_filter)
				),
				TextButton(
					text="Aceptar",
					on_click=self.apply_filters
				)
			],
			on_dismiss=lambda _: self.page.close(self.dlg_sites_filter)
		)

		self.gl: Geolocator = Geolocator(
			location_settings=GeolocatorSettings(
				accuracy=GeolocatorPositionAccuracy.LOW
			),
			on_error=lambda e: page.add(Text(f"Error: {e.data}")),
		)
		page.overlay.append(self.gl)

		self.dlg_request_location_permission: AlertDialog = AlertDialog(
			modal=True,
			title=Text("Permisos de ubicación"),
			content=Text(
				"Para filtrar sitios turísticos por cercanía a tu posición actual, "
				"necesitamos que permitas el acceso a tu ubicación."
			),
			actions=[
				TextButton(
					text="Cancelar",
					on_click=self.handle_cancel_location_permission
				),
				TextButton(
					text="Aceptar",
					on_click=self.handle_accept_location_permission
				)
			],
			actions_alignment=MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_request_location_permission)
		)

		self.dlg_location_permissions_failed: AlertDialog = AlertDialog(
			modal=True,
			title=Text("Permisos de ubicación"),
			content=Text(
				"No se han otorgado los permisos de ubicación, "
				"se ha deshabilitado la opción de filtrado de sitios turísticos por cercanía."
			),
			actions_alignment=MainAxisAlignment.END,
			actions=[
				TextButton(
					text="Aceptar",
					on_click=lambda _: self.page.close(self.dlg_location_permissions_failed)
				)
			],
			on_dismiss=lambda _: self.page.close(self.dlg_location_permissions_failed)
		)

		self.dlg_location_permissions_succeded: AlertDialog = AlertDialog(
			modal=True,
			title=Text("Permisos de ubicación"),
			content=Text(
				"Se han otorgado los permisos de ubicación, "
				"Ahora puedes usar la opción de filtrado de sitios turísticos por cercanía."
			),
			actions_alignment=MainAxisAlignment.END,
			actions=[
				TextButton(
					text="Aceptar",
					on_click=lambda _: self.page.close(self.dlg_location_permissions_succeded)
				)
			],
			on_dismiss=lambda _: self.page.close(self.dlg_location_permissions_succeded)
		)

		# Places and pagination variables
		self.items: list | Container = self.get_places()

		self.current_page: int = 0
		self.items_per_page: int = 10
		self.page_start_index: int = 0
		self.page_end_index: int = self.items_per_page

		self.lv_places_list: ListView = ListView(
			padding=padding.symmetric(
				vertical=(SPACING / 2),
				horizontal=SPACING
			),
			spacing=(SPACING / 2),
			controls=(
				self.items
				if isinstance(self.items, Container)
				else self.items[self.page_start_index:self.page_end_index]
			)
		)

		self.total_items: int = len(self.items)
		self.total_pages: int = (self.total_items + self.items_per_page - 1) // self.items_per_page
		self.lbl_actual_page: Text = Text(
			value=f"Página {self.current_page + 1} de {self.total_pages}",
			color=colors.BLACK
		)
		self.cont_pagination: Container = Container(
			width=self.page.width,
			margin=margin.only(bottom=5),
			alignment=alignment.center,
			content=Row(
				controls=[
					Container(
						margin=margin.only(left=SPACING - 5),
						content=Icon(
							name=icons.ARROW_BACK_IOS_SHARP,
							size=25,
							color=colors.BLACK
						),
						on_click=self.previous_page
					),
					Container(
						expand=True,
						alignment=alignment.center,
						content=self.lbl_actual_page
					),
					Container(
						margin=margin.only(right=SPACING - 5),
						content=Icon(
							name=icons.ARROW_FORWARD_IOS_SHARP,
							size=25,
							color=colors.BLACK
						),
						on_click=self.next_page
					),
				]
			)
		)

		return View(
			route=self.route,
			bgcolor=colors.WHITE,
			padding=padding.all(value=0.0),
			spacing=0,
			controls=[
				TopBar(page=self.page, leading=False, logger=logger),
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
					height=TXT_CONT_SIZE,
					margin=margin.symmetric(vertical=10),
					content=Row(
						controls=[
							Container(expand=1),
							Container(
								expand=8,
								bgcolor=colors.WHITE,
								padding=padding.symmetric(
									horizontal=(SPACING / 2)
								),
								border_radius=border_radius.all(
									value=RADIUS
								),
								shadow=BoxShadow(
									blur_radius=(BLUR / 2),
									offset=Offset(0, 2),
									color=colors.GREY
								),
								content=Row(
									alignment=MainAxisAlignment.SPACE_BETWEEN,
									spacing=None,
									controls=[
										Container(
											expand=4,
											content=self.txt_place_searcher,
										),
										Container(
											expand=1,
											content=CircleAvatar(
												bgcolor=colors.WHITE,
												radius=SPACING,
												content=Icon(
													name=icons.FILTER_LIST,
													color=colors.BLACK
												)
											),
											on_click=lambda _:
												self.page.open(self.dlg_sites_filter)
										)
									]
								)
							),
							Container(expand=1),
						]
					)
				),
				self.cont_pagination,
				Container(
					expand=True,
					width=self.page.width,
					content=self.lv_places_list
				),
				BottomBar(
					page=self.page,
					logger=logger,
					current_route=self.route
				)
			]
		)

	def get_places(
		self,
		category: str = None,
		municipality: str =  None,
		distance: int = None,
		current_position: tuple[float, float] = None
	) -> list | Container:
		logger.info("Calling Back-End API...")
		response: Response = get(
			url=f"{BACK_END_URL}/{GET_DEMO_DATA_ENDPOINT}",
			headers={
				"Content-Type": "application/json",
				"Authorization": f"Bearer {self.basket.get('session_token')}"
			},
			json={
				"category": category,
				"municipality": municipality,
				"distance": distance,
				"current_position": current_position
			}
		)

		logger.info("Evaluating response...")
		if response.status_code == 200:
			places_data: dict = response.json()["data"]
			logger.info(f"Obtained a total of {len(places_data)} places...")
			return [
				PlaceCard(
					page=self.page,
					title=place["name"],
					category=place["classification"],
					punctuation=place["punctuation"],
					image_link=self.get_place_image(place["name"]),
					address=(
						f"{place['street_number']}, "
						f"{place['colony']}, "
						f"{place['cp']}, "
						f"{place['municipality']}, "
						f"{place['state']}."
					),
					distance=place["distance"] if "distance" in place else None
				)
				for place in places_data
			]

		elif response.status_code == 204:
			return [
				Container(
					alignment=alignment.center,
					content=Text(
						value=(
							"No se encontró ningún sitio turístico con "
							"los filtros seleccionados."
						),
						color=colors.BLACK,
						size=30
					)
				)
			]

		else:
			return [
				Container(
					alignment=alignment.center,
					content=Text(
						value=(
							"Ocurrió un error al obtener la información de "
							"los sitios turísticos."
						),
						color=colors.BLACK,
						size=30
					)
				)
			]

	def get_place_image(self, place_name: str) -> str:
		dir: str = format_place_name(place_name)

		path: str = join(ASSETS_ABSPATH, "places", dir)
		if os.path.exists(path):
			images: list = listdir(path)
			if images:
				return join("places", dir, images[0])
			else:
				return ["/default.png"]
		else:
			return ["/default.png"]

	def hide_show_slider(self, _: ControlEvent) -> None:
		logger.info("Checking location permissions...")
		if not is_location_permission_enabled(self.gl, logger):
			logger.warning("Location permissions are not granted...")
			logger.info("Requesting location permissions...")
			self.page.open(self.dlg_request_location_permission)

		else:
			logger.info("Location permissions are granted...")
			logger.info("Updating slider status...")
			self.sld_distance.disabled = not self.chk_distance.value
			self.page.update()

	def handle_accept_location_permission(self, _: ControlEvent) -> None:
		if request_location_permissions(self.gl, logger):
			logger.info("Location permissions granted...")
			logger.info("Allowing distance filter...")
			self.chk_distance.value = True
			self.sld_distance.disabled = False
			self.page.update()
			self.page.open(self.dlg_location_permissions_succeded)

		else:
			logger.warning("Location permissions denied...")
			logger.info("Opening location permissions failed dialog...")
			self.chk_distance.value = False
			self.sld_distance.disabled = True
			self.page.update()
			self.page.open(self.dlg_location_permissions_failed)
			# self.open_location_permissions_failed_dialog()

	# def open_location_permissions_failed_dialog(self) -> None:
	# 	self.chk_distance.value = False
	# 	self.sld_distance.disabled = True
	# 	self.page.update()
	# 	self.page.open(self.dlg_location_permissions_failed)

	def handle_cancel_location_permission(self, _: ControlEvent) -> None:
		logger.warning("User canceled location permission request...")
		logger.info("Closing location permission alert dialog and cleaning filter...")
		self.page.close(self.dlg_request_location_permission)
		self.chk_distance.value = False
		self.sld_distance.disabled = True
		self.page.update()

	def update_pagination_data(self, items: list) -> None:
		self.current_page = 0
		self.total_items = len(items)
		self.total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
		self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
		self.page.update()

	def search_place(self, _: ControlEvent) -> None:
		if self.txt_place_searcher.value == "":
			logger.info("Cleaning 'searching place' filter...")
			self.lv_places_list.controls = self.items[0:self.items_per_page]
			self.update_pagination_data(self.items)
		else:
			value = self.txt_place_searcher.value.lower()
			logger.info(f"Searching place... Searching for value {value}")
			items = [
				place for place in self.items if value in
				# Searching in the structure of the PlaceCard component in place_card.py
				place.content.controls[0].content.controls[0].value.lower()
			]
			self.lv_places_list.controls = items[0:self.items_per_page]
			self.update_pagination_data(items)

	def clean_filters(self, _: ControlEvent) -> None:
		logger.info("Cleaning filters...")
		self.page.close(self.dlg_sites_filter)
		self.drd_categories.value = None
		self.drd_municipality.value = None
		self.items: list = self.get_places()
		self.lv_places_list.controls = self.items[0:self.items_per_page]
		self.chk_distance.value = False
		self.sld_distance.value = 5
		self.sld_distance.disabled = True
		self.update_pagination_data(self.items)
		self.page.update()

	def apply_filters(self, _: ControlEvent) -> None:
		self.page.close(self.dlg_sites_filter)
		logger.info("Applying filters...")

		if self.chk_distance.value:
			logger.info("Checking location permissions...")
			if not self.gl.is_location_service_enabled():
				logger.warning("Location services are not enabled...")
				logger.info("Requesting location services...")
				self.gl.open_location_settings()
			else:
				logger.info("Location services are enabled...")

				logger.info("Checking if user's location is inside CDMX coordinates...")
				position = self.gl.get_current_position()

				# if is_inside_cdmx((position.latitude, position.longitude)):
				# 	logger.info("User's location is inside CDMX coordinates...")
				# 	distance: int = self.sld_distance.value
				# 	current_position: tuple[float, float] = position.latitude, position.longitude

				# else:
				# 	logger.warning("User's location is not inside CDMX coordinates...")
				# 	distance = None
				# 	current_position = None
				distance: int = int(self.sld_distance.value)
				current_position: tuple[float, float] = position.latitude, position.longitude
				logger.info(f"User's location: {current_position}")

		else:
			logger.info("User did not select the distance filter. Skipping...")
			distance = None
			current_position = None

		logger.info("Modifying db consult conditions...")
		#! if self.drd_categories.value or self.drd_municipality.value:

		self.items: list = self.get_places(
			category=(
				self.drd_categories.value
				if self.drd_categories.value != ""
				else None
			),
			municipality=(
				self.drd_municipality.value
				if self.drd_municipality.value != ""
				else None
			),
			distance=distance,
			current_position=current_position
		)

		if isinstance(self.items[0], PlaceCard):
			self.lv_places_list.controls = self.items[0:self.items_per_page]
		else:
			self.lv_places_list.controls = self.items

		self.update_pagination_data(self.items)
		self.page.update()

	def set_page_indexes(self) -> None:
		self.page_start_index = self.current_page * self.items_per_page
		self.page_end_index = self.page_start_index + self.items_per_page
		self.lv_places_list.controls = self.items[self.page_start_index:self.page_end_index]

	def previous_page(self, _: ControlEvent) -> None:
		logger.info(f"Going to previous page...")
		if self.current_page > 0:
			self.current_page -= 1
		else:
			self.current_page = self.total_pages - 1

		self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
		self.set_page_indexes()
		self.page.update()

	def next_page(self, _: ControlEvent) -> None:
		logger.info(f"Going to next page...")
		if self.current_page < self.total_pages - 1:
			self.current_page += 1
		else:
			self.current_page = 0

		self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
		self.set_page_indexes()
		self.page.update()
