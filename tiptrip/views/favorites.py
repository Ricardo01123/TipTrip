import flet as ft
from requests import get, Response
from logging import Logger, getLogger

from components.bars import *
from resources.config import *
from resources.functions import *
from components.place_card import PlaceCard
from resources.styles import txt_messages_style


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class FavoritesView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page

		# Custom components
		# Geolocation components
		self.gl: ft.Geolocator = ft.Geolocator(
			location_settings=ft.GeolocatorSettings(
				accuracy=ft.GeolocatorPositionAccuracy.LOW
			),
			on_error=lambda error: logger.error(f"Geolocator error: {error}"),
		)
		self.page.overlay.append(self.gl)

		self.txt_favorite_searcher: ft.TextField = ft.TextField(
			prefix_icon=ft.Icons.SEARCH,
			hint_text="Busca un sitio favorito",
			on_change=self.search_favorite,
			**txt_messages_style
		)

		# Places and pagination variables
		self.items: list | ft.Container = self.get_favorites()

		self.current_page: int = 0
		self.items_per_page: int = 10
		self.page_start_index: int = 0
		self.page_end_index: int = self.items_per_page

		self.lv_favorites_list: ft.ListView = ft.ListView(
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
			color=ft.Colors.BLACK
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
							name=ft.Icons.ARROW_BACK_IOS_SHARP,
							size=25,
							color=ft.Colors.BLACK
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
							name=ft.Icons.ARROW_FORWARD_IOS_SHARP,
							size=25,
							color=ft.Colors.BLACK
						),
						on_click=self.next_page
					),
				]
			)
		)

		# Modals and bottom sheet components
		self.dlg_request_location_permission: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text(""),
			content=ft.Text(""),
			actions=[
				ft.TextButton(
					text="Cancelar",
					on_click=lambda _: self.page.close(self.dlg_request_location_permission)
				),
				ft.TextButton(
					text="Aceptar",
					on_click=self.request_location_permission
				)
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_request_location_permission)
		)
		self.dlg_location: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text(""),
			content=ft.Text(""),
			actions_alignment=ft.MainAxisAlignment.END,
			actions=[
				ft.TextButton(
					text="Aceptar",
					on_click=lambda _: self.page.close(self.dlg_location)
				)
			],
			on_dismiss=lambda _: self.page.close(self.dlg_location)
		)
		self.dlg_error: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text(""),
			content=ft.Text(""),
			actions=[
				ft.TextButton("Aceptar", on_click=lambda _: self.page.close(self.dlg_error)),
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_error)
		)

		# View native attributes
		super().__init__(
			route="/favorites",
			bgcolor=ft.Colors.WHITE,
			padding=ft.padding.all(value=0.0),
			spacing=0,
			floating_action_button=ft.FloatingActionButton(
				icon=ft.Icons.LOCATION_ON,
				bgcolor=SECONDARY_COLOR,
				foreground_color=ft.Colors.WHITE,
				shape=ft.CircleBorder(),
				on_click=self.check_if_open_map
			),
			floating_action_button_location=ft.FloatingActionButtonLocation.MINI_CENTER_DOCKED,
			controls=[
				TopBar(page=self.page, leading=True, logger=logger),
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
						color=ft.Colors.GREY_800
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
								bgcolor=ft.Colors.WHITE,
								padding=ft.padding.symmetric(
									horizontal=(SPACING / 2)
								),
								border_radius=ft.border_radius.all(
									value=RADIUS
								),
								shadow=ft.BoxShadow(
									blur_radius=(BLUR / 2),
									offset=ft.Offset(0, 2),
									color=ft.Colors.GREY
								),
								alignment=ft.alignment.center_left,
								content=self.txt_favorite_searcher
							),
							ft.Container(expand=1),
						]
					)
				),
				self.cont_pagination,
				ft.Container(
					expand=True,
					width=self.page.width,
					content=self.lv_favorites_list
				)
			],
			bottom_appbar=BottomBar(page=self.page, logger=logger, current_route="/favorites")
		)

	def get_favorites(self) -> list | ft.Container:
		logger.info("Calling Back-End API...")

		response: Response = get(
			url=f"{BACK_END_URL}/{FAVORITES_ENDPOINT}/{self.page.session.get('id')}",
			headers={
				"Content-Type": "application/json",
				"Authorization": f"Bearer {self.page.session.get('session_token')}"
			},
			json={
				"current_latitude": self.page.session.get("current_latitude"),
				"current_longitude": self.page.session.get("current_longitude")
			}
		)

		logger.info("Evaluating response...")
		if response.status_code == 200:
			favorites: dict = response.json()["favorites"]
			logger.info(f"Obtained a total of {len(favorites)} favorite places...")
			return [
				PlaceCard(
					page=self.page,
					id=favorite["id"],
					name=favorite["name"],
					classification=favorite["classification"],
					address=favorite["address"],
					image_name=get_placecard_image(favorite["name"]),
					is_favorite=True,
					punctuation=favorite["punctuation"],
					distance=favorite["distance"],
				)
				for favorite in favorites
			]

		elif response.status_code == 204:
			return [
				ft.Container(
					alignment=ft.alignment.center,
					content=ft.Text(
						value="No se encontró ningún sitio turístico favorito.",
						color=ft.Colors.BLACK,
						size=30
					)
				)
			]

		else:
			return [
				ft.Container(
					alignment=ft.alignment.center,
					content=ft.Text(
						value=(
							"Ocurrió un error al obtener la lista de sitios "
							"turísticos favoritos.\nFavor de intentarlo de nuevo "
							"más tarde."
						),
						color=ft.Colors.BLACK,
						size=30
					)
				)
			]

	def update_pagination_data(self, items: list) -> None:
		self.current_page = 0
		self.total_items = len(items)
		self.total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
		self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
		self.page.update()

	def search_favorite(self, _: ft.ControlEvent) -> None:
		if self.txt_favorite_searcher.value == "":
			logger.info("Cleaning 'searching favorite' filter...")
			self.lv_favorites_list.controls = self.items[0:self.items_per_page]
			self.update_pagination_data(self.items)
		else:
			value: str = self.txt_favorite_searcher.value.lower()
			logger.info(f"Searching favorite... Searching for value {value}")
			items: list = [
				favorite for favorite in self.items if value in
				# Searching in the structure of the PlaceCard component in place_card.py
				favorite.content.controls[0].content.controls[0].value.lower()
			]
			self.lv_favorites_list.controls = items[0:self.items_per_page]
			self.update_pagination_data(items)

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

	def request_location_permission(self, _: ft.ControlEvent) -> None:
		self.page.close(self.dlg_request_location_permission)

		logger.info("Requesting location permissions...")
		if request_location_permissions(self.gl, logger):
			logger.info("Location permissions granted. Getting current coordinates...")
			current_position: ft.GeolocatorPosition = self.gl.get_current_position()
			self.page.session.set(key="current_latitude", value=current_position.latitude)
			self.page.session.set(key="current_longitude", value=current_position.longitude)
			logger.info(f"Got current coordinates: ({current_position.latitude}, {current_position.longitude})")

			logger.info("Verifying if user's location is inside CDMX coordinates...")
			if is_inside_cdmx((self.page.session.get("current_latitude"), self.page.session.get("current_longitude"))):
				logger.info("User's location is inside CDMX coordinates. Allowing distance filter...")
				self.page.session.set(key="is_inside_cdmx", value=True)
				self.page.session.set(key="chk_distance_value", value=True)

			else:
				logger.warning("User's location is not inside CDMX coordinates")
				self.dlg_location.title = ft.Text("Ubicación fuera de CDMX")
				self.dlg_location.content = ft.Text(
					"Tu ubicación actual no se encuentra dentro de los límites de la Ciudad de México, "
					"por lo que no se puede aplicar el filtro de cercanía."
				)
				self.page.open(self.dlg_location)

		else:
			logger.warning("Location permissions denied. Opening location permissions failed dialog...")
			self.dlg_location.title = ft.Text("Permisos de ubicación")
			self.dlg_location.content = ft.Text(
				"No se han otorgado los permisos de ubicación, "
				"se ha deshabilitado la opción de filtrado de sitios turísticos por cercanía."
			)
			self.page.open(self.dlg_location)

	def check_if_open_map(self, _: ft.ControlEvent) -> None:
		logger.info("Checking location permissions...")
		if self.gl.is_location_service_enabled():
			logger.info("Location permissions are granted...")
			go_to_view(self.page, logger=logger, route="/map")

		else:

			logger.warning("Location permissions are not granted...")
			logger.info("Requesting location permissions...")
			self.dlg_request_location_permission.content = ft.Text(
				"Para acceder al mapa interactivo, "
				"necesitamos que permitas el acceso a tu ubicación."
			)
			self.page.open(self.dlg_request_location_permission)
