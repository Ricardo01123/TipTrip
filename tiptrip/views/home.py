import flet as ft
from requests import get, Response
from logging import Logger, getLogger

from components.bars import *
from resources.config import *
from resources.functions import *
from components.place_card import PlaceCard
from resources.styles import txt_messages_style


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class HomeView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page

		# Custom components
		# Filters components
		self.txt_place_searcher: ft.TextField = ft.TextField(
			prefix_icon=ft.icons.SEARCH,
			hint_text="Busca un sitio turístico",
			on_change=self.search_place,
			**txt_messages_style
		)
		self.drd_municipality: ft.Dropdown = ft.Dropdown(
			label="Filtrar por delegación",
			options=[
				ft.dropdown.Option(municipality)
				for municipality in MUNICIPALITIES
			]
		)
		self.drd_classification: ft.Dropdown = ft.Dropdown(
			label="Filtrar por clasificación",
			options=[
				ft.dropdown.Option(classification)
				for classification in CLASSIFICATIONS
			]
		)
		self.sld_distance: ft.Slider = ft.Slider(
			min=1,
			max=15,
			value=7,
			divisions=5,
			label="{value} km",
			disabled=True
		)
		self.chk_distance: ft.Checkbox = ft.Checkbox(
			label="Filtrar por cercanía",
			value=False,
			on_change=self.hide_show_slider
		)
		self.dlg_sites_filter: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			adaptive=True,
			title=ft.Text("Filtrar sitios turísticos"),
			content=ft.Column(
				controls=[
					ft.Container(content=self.drd_classification),
					ft.Container(content=self.drd_municipality),
					ft.Container(content=self.chk_distance),
					ft.Container(content=self.sld_distance),
					ft.Container(
						content=ft.TextButton(
							text="Eliminar filtros",
							on_click=self.clean_filters
						)
					)
				]
			),
			actions=[
				ft.TextButton(
					text="Cancelar",
					on_click=lambda _: self.page.close(self.dlg_sites_filter)
				),
				ft.TextButton(
					text="Aceptar",
					on_click=self.apply_filters
				)
			],
			on_dismiss=lambda _: self.page.close(self.dlg_sites_filter)
		)

		# Geolocation components
		self.gl: ft.Geolocator = ft.Geolocator(
			location_settings=ft.GeolocatorSettings(
				accuracy=ft.GeolocatorPositionAccuracy.LOW
			),
			on_error=lambda error: logger.error(f"Geolocator error: {error}"),
		)
		self.page.overlay.append(self.gl)

		# Modals components
		self.dlg_request_location_permission: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Permisos de ubicación"),
			content=ft.Text(
				"Para filtrar sitios turísticos por cercanía a tu posición actual, "
				"necesitamos que permitas el acceso a tu ubicación."
			),
			actions=[
				ft.TextButton(
					text="Cancelar",
					on_click=self.handle_cancel_location_permission
				),
				ft.TextButton(
					text="Aceptar",
					on_click=self.handle_accept_location_permission
				)
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_request_location_permission)
		)
		self.dlg_location_permissions_failed: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Permisos de ubicación"),
			content=ft.Text(
				"No se han otorgado los permisos de ubicación, "
				"se ha deshabilitado la opción de filtrado de sitios turísticos por cercanía."
			),
			actions_alignment=ft.MainAxisAlignment.END,
			actions=[
				ft.TextButton(
					text="Aceptar",
					on_click=lambda _: self.page.close(self.dlg_location_permissions_failed)
				)
			],
			on_dismiss=lambda _: self.page.close(self.dlg_location_permissions_failed)
		)
		self.dlg_location_permissions_succeded: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Permisos de ubicación"),
			content=ft.Text(
				"Se han otorgado los permisos de ubicación, "
				"Ahora puedes usar la opción de filtrado de sitios turísticos por cercanía."
			),
			actions_alignment=ft.MainAxisAlignment.END,
			actions=[
				ft.TextButton(
					text="Aceptar",
					on_click=lambda _: self.page.close(self.dlg_location_permissions_succeded)
				)
			],
			on_dismiss=lambda _: self.page.close(self.dlg_location_permissions_succeded)
		)
		self.dlg_location_outside_cdmx: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Ubicación fuera de CDMX"),
			content=ft.Text(
				"Tu ubicación actual no se encuentra dentro de los límites de la Ciudad de México, "
				"por lo que no se puede aplicar el filtro de cercanía."
			),
			actions_alignment=ft.MainAxisAlignment.END,
			actions=[
				ft.TextButton(
					text="Aceptar",
					on_click=lambda _: self.page.close(self.dlg_location_outside_cdmx)
				)
			],
			on_dismiss=lambda _: self.page.close(self.dlg_location_outside_cdmx)
		)

		# Places and pagination variables
		self.items: list | ft.Container = self.get_places()

		self.current_page: int = 0
		self.items_per_page: int = 10
		self.page_start_index: int = 0
		self.page_end_index: int = self.items_per_page

		self.lv_places_list: ft.ListView = ft.ListView(
			padding=ft.padding.symmetric(
				vertical=(SPACING / 2),
				horizontal=SPACING
			),
			spacing=(SPACING / 2),
			controls=(
				self.items
				if isinstance(self.items, ft.Container)
				else self.items[self.page_start_index:self.page_end_index]
			)
		)

		self.total_items: int = len(self.items)
		self.total_pages: int = (self.total_items + self.items_per_page - 1) // self.items_per_page
		self.lbl_actual_page: ft.Text = ft.Text(
			value=f"Página {self.current_page + 1} de {self.total_pages}",
			color=ft.colors.BLACK
		)
		self.cont_pagination: ft.Container = ft.Container(
			width=self.page.width,
			margin=ft.margin.only(bottom=5),
			alignment=ft.alignment.center,
			content=ft.Row(
				controls=[
					ft.Container(
						margin=ft.margin.only(left=SPACING - 5),
						content=ft.Icon(
							name=ft.icons.ARROW_BACK_IOS_SHARP,
							size=25,
							color=ft.colors.BLACK
						),
						on_click=self.previous_page
					),
					ft.Container(
						expand=True,
						alignment=ft.alignment.center,
						content=self.lbl_actual_page
					),
					ft.Container(
						margin=ft.margin.only(right=SPACING - 5),
						content=ft.Icon(
							name=ft.icons.ARROW_FORWARD_IOS_SHARP,
							size=25,
							color=ft.colors.BLACK
						),
						on_click=self.next_page
					)
				]
			)
		)

		# View native attributes
		super().__init__(
			route='/',
			bgcolor=ft.colors.WHITE,
			padding=ft.padding.all(value=0.0),
			spacing=0,
			controls=[
				TopBar(page=self.page, leading=False, logger=logger),
				ft.Container(
					width=self.page.width,
					height=RADIUS,
					bgcolor=MAIN_COLOR,
					border_radius=ft.border_radius.only(
						bottom_left=RADIUS,
						bottom_right=RADIUS
					),
					shadow=ft.BoxShadow(
						blur_radius=BLUR,
						color=ft.colors.GREY_800
					)
				),
				ft.Container(
					width=self.page.width,
					height=TXT_CONT_SIZE,
					margin=ft.margin.symmetric(vertical=10),
					content=ft.Row(
						controls=[
							ft.Container(expand=1),
							ft.Container(
								expand=8,
								bgcolor=ft.colors.WHITE,
								padding=ft.padding.symmetric(horizontal=(SPACING / 2)),
								border_radius=ft.border_radius.all(value=RADIUS),
								shadow=ft.BoxShadow(
									blur_radius=(BLUR / 2),
									offset=ft.Offset(0, 2),
									color=ft.colors.GREY
								),
								content=ft.Row(
									alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
									spacing=None,
									controls=[
										ft.Container(
											expand=4,
											content=self.txt_place_searcher,
										),
										ft.Container(
											expand=1,
											content=ft.CircleAvatar(
												bgcolor=ft.colors.WHITE,
												radius=SPACING,
												content=ft.Icon(
													name=ft.icons.FILTER_LIST,
													color=ft.colors.BLACK
												)
											),
											on_click=lambda _: self.page.open(self.dlg_sites_filter)
										)
									]
								)
							),
							ft.Container(expand=1),
						]
					)
				),
				self.cont_pagination,
				ft.Container(
					expand=True,
					width=self.page.width,
					content=self.lv_places_list
				),
				BottomBar(page=self.page, logger=logger, current_route='/')
			]
		)

	def get_places(
		self,
		classification: str = None,
		municipality: str =  None,
		distance: int = None,
		current_latitude: float = None,
		current_longitude: float = None
	) -> list | ft.Container:
		logger.info("Calling Back-End API...")
		response: Response = get(
			url=f"{BACK_END_URL}/{PLACES_ENDPOINT}",
			headers={
				"Content-Type": "application/json",
				"Authorization": f"Bearer {self.page.session.get('session_token')}"
			},
			json={
				"classification": classification,
				"municipality": municipality,
				"distance": distance,
				"current_latitude": current_latitude,
				"current_longitude": current_longitude
			}
		)

		logger.info("Evaluating response...")
		if response.status_code == 200:
			places: dict = response.json()["places"]
			logger.info(f"Obtained a total of {len(places)} places...")
			return [
				PlaceCard(
					page=self.page,
					id=place["id"],
					name=place["info"]["name"],
					classification=place["info"]["classification"],
					address=(
						f"{place['address']['street_number']}, "
						f"{place['address']['colony']}, "
						f"{place['address']['cp']}, "
						f"{place['address']['municipality']}, "
						f"{place['address']['state']}."
					),
					image_link=get_place_image(place["info"]["name"]),
					is_favorite=place["is_favorite"],
					punctuation=place["info"]["punctuation"],
					distance=place["distance"] if "distance" in place else None
				)
				for place in places
			]

		elif response.status_code == 204:
			logger.info(f"Places endpoint response received {response.status_code}: {response.json()}")
			return [
				ft.Container(
					alignment=ft.alignment.center,
					content=ft.Text(
						value=(
							"No se encontró ningún sitio turístico con "
							"los filtros seleccionados."
						),
						color=ft.colors.BLACK,
						size=30
					)
				)
			]

		else:
			logger.info(f"Places endpoint response received {response.status_code}: {response.json()}")
			return [
				ft.Container(
					alignment=ft.alignment.center,
					content=ft.Text(
						value=(
							"Ocurrió un error al obtener la información de "
							"los sitios turísticos."
						),
						color=ft.colors.BLACK,
						size=30
					)
				)
			]

	def hide_show_slider(self, _: ft.ControlEvent) -> None:
		logger.info("Checking location permissions...")
		if is_location_permission_enabled(self.gl, logger):
			logger.info("Location permissions are granted...")
			logger.info("Updating slider status...")
			self.sld_distance.disabled = not self.chk_distance.value
			self.page.update()

		else:
			logger.warning("Location permissions are not granted...")
			logger.info("Requesting location permissions...")
			self.page.open(self.dlg_request_location_permission)

	def handle_accept_location_permission(self, _: ft.ControlEvent) -> None:
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

	def handle_cancel_location_permission(self, _: ft.ControlEvent) -> None:
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
		# if self.total_pages == 0:
		# 	self.cont_pagination.visible = False
		# else:
		self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
		self.page.update()

	def search_place(self, _: ft.ControlEvent) -> None:
		if self.txt_place_searcher.value == "":
			logger.info("Cleaning 'searching place' filter...")
			self.lv_places_list.controls = self.items[0:self.items_per_page]
			self.update_pagination_data(self.items)
		else:
			value: str = self.txt_place_searcher.value.lower()
			logger.info(f"Searching place... Searching for value {value}")
			items: list = [
				place for place in self.items if value in
				# Searching in the structure of the PlaceCard component in place_card.py
				place.content.controls[0].content.controls[0].value.lower()
			]
			self.lv_places_list.controls = items[0:self.items_per_page]
			self.update_pagination_data(items)

	def clean_filters(self, _: ft.ControlEvent) -> None:
		logger.info("Cleaning filters...")
		self.page.close(self.dlg_sites_filter)
		self.drd_classification.value = None
		self.drd_municipality.value = None
		self.items: list = self.get_places()
		self.lv_places_list.controls = self.items[0:self.items_per_page]
		self.chk_distance.value = False
		self.sld_distance.value = 5
		self.sld_distance.disabled = True
		self.update_pagination_data(self.items)
		self.page.update()

	def apply_filters(self, _: ft.ControlEvent) -> None:
		self.page.close(self.dlg_sites_filter)
		logger.info("Applying filters...")

		if self.chk_distance.value:
			logger.info("Checking location permissions...")
			if not is_location_permission_enabled(self.gl, logger):
				logger.warning("Location permissions are not granted...")
				logger.info("Requesting location permissions...")
				self.page.open(self.dlg_request_location_permission)

			else:
				logger.info("Location permissions are granted...")
				logger.info("Getting user's location...")
				position = self.gl.get_current_position()
				current_latitude: float = position.latitude
				current_longitude: float = position.longitude
				logger.info(f"User's location: ({current_latitude}, {current_longitude})")

				logger.info("Checking if user's location is inside CDMX coordinates...")
				if is_inside_cdmx((current_latitude, current_longitude)):
					logger.info("User's location is inside CDMX coordinates. Continuing...")
					distance: int = int(self.sld_distance.value)

				else:
					logger.warning("User's location is not inside CDMX coordinates. Skipping...")
					distance = None
					current_latitude = None
					current_longitude = None
					self.page.open(self.dlg_location_outside_cdmx)

		else:
			logger.info("User did not select the distance filter. Skipping...")
			distance = None
			current_latitude = None
			current_longitude = None

		logger.info("Modifying db consult conditions...")
		self.items: list = self.get_places(
			classification=(
				self.drd_classification.value
				if self.drd_classification.value != ""
				else None
			),
			municipality=(
				self.drd_municipality.value
				if self.drd_municipality.value != ""
				else None
			),
			distance=distance,
			current_latitude=current_latitude,
			current_longitude=current_longitude
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

	def previous_page(self, _: ft.ControlEvent) -> None:
		logger.info(f"Going to previous page...")
		if self.current_page > 0:
			self.current_page -= 1
		else:
			self.current_page = self.total_pages - 1

		self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
		self.set_page_indexes()
		self.page.update()

	def next_page(self, _: ft.ControlEvent) -> None:
		logger.info(f"Going to next page...")
		if self.current_page < self.total_pages - 1:
			self.current_page += 1
		else:
			self.current_page = 0

		self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
		self.set_page_indexes()
		self.page.update()
