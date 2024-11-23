import flet as ft
import flet.map as map
from typing import Optional
from requests import get, Response
from geopy.distance import geodesic
from logging import Logger, getLogger

from resources.config import *
from resources.functions import *
from components.bars import TopBar
from resources.config import PROJECT_NAME


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class MapView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page

		# Geolocator components
		self.gl: ft.Geolocator = ft.Geolocator(
			location_settings=ft.GeolocatorSettings(
				accuracy=ft.GeolocatorPositionAccuracy.LOW
			),
			on_error=lambda error: logger.error(f"Geolocator error: {error}"),
		)
		self.page.overlay.append(self.gl)

		# Map components
		self.markers_names_are_hidden: bool = True
		self.circle_layer = map.CircleLayer(circles=[self.create_circle_marker()])
		self.marker_layer = map.MarkerLayer(
			markers=[
				*self.create_places_markers(self.get_places()),
				self.create_user_marker()
			]
		)
		self.map = self.create_map()

		# Dialogs components
		self.dlg_place_info: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text(""),
			content=ft.Text(""),
			actions=[
				ft.TextButton(
					text="Cerrar",
					on_click=lambda _: self.page.close(self.dlg_place_info)
				),
				ft.TextButton(
					text="Ver detalles",
					on_click=lambda _: go_to_view(self.page, logger=logger, route="/place_details")
				),
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_place_info)
		)
		self.dlg_request_location_permission: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Permisos de ubicación"),
			content=ft.Text(
				"Para centrar el mapa en tu ubicación, "
				"necesitamos que permitas el acceso a tu ubicación."
			),
			actions=[
				ft.TextButton(
					text="Cancelar",
					on_click=lambda _: self.page.close(self.dlg_request_location_permission)
				),
				ft.TextButton(
					text="Aceptar",
					on_click=self.handle_accept_location_permission
				)
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_request_location_permission)
		)
		self.dlg_location_permissions_succeded: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Permisos de ubicación"),
			content=ft.Text(
				"Se han otorgado los permisos de ubicación, "
				"Ahora se puede centrar el mapa con base en la ubicación actual."
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
		self.dlg_location_permissions_failed: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Permisos de ubicación"),
			content=ft.Text(
				"No se han otorgado los permisos de ubicación, "
				"No se ha podido centrar el mapa con base en la ubicación actual."
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

		# Settings components
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
			active_color=SECONDARY_COLOR,
			thumb_color=SECONDARY_COLOR
		)
		self.ext_settings: ft.ExpansionTile = ft.ExpansionTile(
			trailing=ft.Icon(
				name=ft.icons.KEYBOARD_ARROW_DOWN,
				color=ft.colors.BLACK,
				size=22
			),
			title=ft.Text(
				value="Filtrar sitios turísticos",
				color=ft.colors.BLACK,
				size=16
			),
			tile_padding=ft.padding.symmetric(horizontal=SPACING),
			controls=[
				ft.Container(
					padding=ft.padding.symmetric(horizontal=SPACING),
					content=self.drd_classification,
				),
				ft.ListTile(
					content_padding=ft.padding.symmetric(horizontal=SPACING),
					title=ft.Text(
						value="Distancia de mí:",
						color=ft.colors.BLACK,
						size=16
					)
				),
				ft.Container(content=self.sld_distance),
				ft.Container(
					margin=ft.margin.symmetric(vertical=(SPACING / 2)),
					padding=ft.padding.symmetric(horizontal=SPACING),
					content=ft.Row(
						alignment=ft.MainAxisAlignment.SPACE_AROUND,
						controls=[
							ft.ElevatedButton(
								bgcolor=SECONDARY_COLOR,
								color=ft.colors.WHITE,
								text="Limpiar filtros",
								on_click=self.clean_filters,
							),
							ft.ElevatedButton(
								bgcolor=SECONDARY_COLOR,
								color=ft.colors.WHITE,
								text="Aplicar filtros",
								on_click=self.apply_filters,
							)
						]
					)
				)
			]
		)

		# View native attributes
		super().__init__(
			route = "/map",
			bgcolor=MAIN_COLOR,
			padding=ft.padding.all(value=0.0),
			spacing=0,
			floating_action_button=ft.FloatingActionButton(
				icon=ft.icons.MY_LOCATION,
				bgcolor=MAIN_COLOR,
				foreground_color=ft.colors.WHITE,
				shape=ft.CircleBorder(),
				on_click=self.center_user
			),
			floating_action_button_location=ft.FloatingActionButtonLocation.MINI_END_FLOAT,
			controls = [
				TopBar(page=self.page, leading=True, logger=logger),
				ft.Container(
					width=self.page.width,
					bgcolor=MAIN_COLOR,
					shadow=ft.BoxShadow(
						blur_radius=BLUR,
						color=ft.colors.GREY_800
					),
					content=self.ext_settings
				),
				self.map
			]
		)

	def get_places(self, distance: int = 20, classification: str = None) -> list | None:
		logger.info("Getting places data...")
		response: Response = get(
			url=f"{BACK_END_URL}/{PLACES_ENDPOINT}",
			headers={
				"Content-Type": "application/json",
				"Authorization": f"Bearer {self.page.session.get('session_token')}"
			},
			json={
				"classification": classification,
				"municipality": None,
				"distance": distance,
				"current_latitude": self.page.session.get("current_latitude"),
				"current_longitude": self.page.session.get("current_longitude")
			}
		)

		logger.info("Evaluating response...")
		data: dict = response.json()
		if response.status_code == 200 and data["places"] != []:
			places: list = response.json()["places"]
			logger.info(f"Obtained a total of {len(places)} places...")
			return places

		elif response.status_code == 204 or data["places"] == []:
			logger.warning("No places found...")
			return []

		else:
			logger.error(f"Places endpoint response received {response.status_code}: {data}")
			return None

	def create_map(self) -> map.Map:
		logger.info("Creating map...")
		return map.Map(
			expand=True,
			configuration=map.MapConfiguration(
				initial_center=map.MapLatitudeLongitude(
					self.page.session.get("current_latitude"),
					self.page.session.get("current_longitude")
				),
				min_zoom=12,
				max_zoom=19,
				initial_zoom=13,
				interaction_configuration=map.MapInteractionConfiguration(
					flags=map.MapInteractiveFlag.ALL
				),
				on_init=lambda _: logger.info("Map initialized successfully"),
				on_tap=self.handle_map_click,
				on_event=self.handle_map_event
			),
			layers=[
				map.TileLayer(
					url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
					on_image_error=lambda error: logger.error(f"TileLayer (MapLayer) error: {error}"),
				),
				map.RichAttribution(
					# alignment=ft.AttributionAlignment.BOTTOM_LEFT,
					attributions=[
						map.TextSourceAttribution(
							text="OpenStreetMap Contributors",
							on_click=lambda e: e.page.launch_url(
								"https://openstreetmap.org/copyright"
							),
						),
						map.TextSourceAttribution(
							text="Flet",
							on_click=lambda e: e.page.launch_url("https://flet.dev"),
						),
					]
				),
				self.marker_layer,
				self.circle_layer
			]
		)

	def create_user_marker(self) -> map.Marker:
		logger.info("Creating user marker...")
		return map.Marker(
			content=ft.Row(
				controls=[
					ft.Icon(
						name=ft.icons.PERSON_PIN_CIRCLE_ROUNDED,
						color=SECONDARY_COLOR,
						size=30
					),
					ft.Text(
						value="Yo",
						size=16,
						color=ft.colors.BLACK,
						weight=ft.FontWeight.BOLD
					),
				],
				spacing=5,
			),
			coordinates=map.MapLatitudeLongitude(
				self.page.session.get("current_latitude"),
				self.page.session.get("current_longitude")
			)
		)

	def create_circle_marker(self, radius: int = 7) -> map.CircleMarker:
		logger.info("Creating circle marker...")
		return map.CircleMarker(
			coordinates=map.MapLatitudeLongitude(
				self.page.session.get("current_latitude"),
				self.page.session.get("current_longitude")
			),
			use_radius_in_meter=True,
			radius=(radius * 1000),
			color=ft.colors.TRANSPARENT,
			border_color=SECONDARY_COLOR,
			border_stroke_width=4,
		)

	def create_places_markers(self, items: list) -> Optional[list]:
		logger.info("Creating places markers...")
		if items is None or items == []:
			logger.warning("No places to create markers...")
			return None

		logger.info(f"Creating {len(items)} markers...")
		return [
			map.Marker(
				content=ft.Row(
					controls=[
						ft.Icon(
							ft.icons.LOCATION_ON_ROUNDED,
							color=ft.colors.RED,
							size=30
						),
						ft.Text(
							value=place["info"]["name"],
							size=16,
							color=ft.colors.BLACK,
							weight=ft.FontWeight.BOLD,
							visible=False
						),
					],
					spacing=5,
				),
				coordinates=map.MapLatitudeLongitude(
					place["address"]["latitude"],
					place["address"]["longitude"]
				),
				data={
					"id": place["id"],
					"name": place["info"]["name"],
					"classification": place["info"]["classification"],
					"address": (
						f"{place['address']['street_number']}, "
						f"{place['address']['colony']}, "
						f"{place['address']['cp']}, "
						f"{place['address']['municipality']}, "
						f"{place['address']['state']}."
					),
					"latitude": place["address"]["latitude"],
					"longitud": place["address"]["longitude"],
					"distancia": place["distance"]
				}
			)
			for place in items
		]

	def center_user(self, _: ft.ControlEvent) -> None:
		try:
			logger.info("Checking location permissions...")
			if self.gl.is_location_service_enabled():
				logger.info("Location permissions granted. Getting current coordinates")
				current_position: ft.GeolocatorPosition = self.gl.get_current_position()
				self.page.session.set(key="current_latitude", value=current_position.latitude)
				self.page.session.set(key="current_longitude", value=current_position.longitude)
				logger.info(f"Got current coordinates: ({current_position.latitude}, {current_position.longitude})")

				logger.info("Centering map on user coordinates...")
				if not self.marker_layer.markers == []:
					self.marker_layer.markers.pop()
				self.map.configuration.initial_center = map.MapLatitudeLongitude(
					self.page.session.get("current_latitude"),
					self.page.session.get("current_longitude")
				)
				self.marker_layer.markers.append(self.create_user_marker())

				logger.info("Adding circle distance radius marker...")
				if not self.circle_layer.circles == []:
					self.circle_layer.circles.pop()
				self.circle_layer.circles.append(
					self.create_circle_marker(radius=self.sld_distance.value)
				)

				logger.info("Creating new map...")
				self.map = self.create_map()

				logger.info("Updating page...")
				self.page.update()

			else:
				logger.warning("Location permissions are not granted. Asking for permissions...")
				self.page.open(self.dlg_request_location_permission)

		except Exception as e:
			logger.error(f"Error centering user on map: {e}")
			self.dlg_error.title.value = "Error al centrar usuario"
			self.dlg_error.content.value = (
				"Ocurrió un error al centrar el mapa en tu ubicación. "
				"Favor de intentarlo de nuevo más tarde."
			)
			self.page.open(self.dlg_error)

	def apply_filters(self, _: ft.ControlEvent) -> None:
		try:
			logger.info("Checking location permissions...")
			if self.gl.is_location_service_enabled():
				logger.info("Location permissions granted")

				logger.info("Getting nearby places...")
				nearby_places: Optional[list] = self.get_places(
					distance=self.sld_distance.value,
					classification=(
						self.drd_classification.value
						if self.drd_classification.value != ""
						else None
					)
				)
				if nearby_places is not None or nearby_places == []:
					if nearby_places == []:
						logger.warning("No places found")
						self.dlg_error.title.value = "Sin resultados"
						self.dlg_error.content.value = "No se encontró ningún lugar turístico con los filtros aplicados."
						self.page.open(self.dlg_error)
						return

					else:
						logger.info("Cleaning previous markers...")
						self.marker_layer.markers = []

						logger.info("Creating new markers...")
						new_places: Optional[list] = self.create_places_markers(nearby_places)
						self.marker_layer.markers = [*new_places]

				else:
					logger.error("Error getting nearby places")
					self.dlg_error.title.value = "Error al aplicar filtros"
					self.dlg_error.content.value = (
						"Ocurrió un error al aplicar los filtros. "
						"Favor de intentarlo de nuevo más tarde."
					)
					self.page.open(self.dlg_error)
					return

				logger.info("Getting current coordinates...")
				current_position: ft.GeolocatorPosition = self.gl.get_current_position()
				self.page.session.set(key="current_latitude", value=current_position.latitude)
				self.page.session.set(key="current_longitude", value=current_position.longitude)
				logger.info(f"Got current coordinates: ({current_position.latitude}, {current_position.longitude})")

				logger.info("Centering map on user coordinates...")
				self.map.configuration.initial_center = map.MapLatitudeLongitude(
					self.page.session.get("current_latitude"),
					self.page.session.get("current_longitude")
				)
				self.marker_layer.markers.append(self.create_user_marker())

				logger.info("Adding circle distance radius marker...")
				if self.circle_layer.circles != []:
					self.circle_layer.circles.pop()
				self.circle_layer.circles.append(
					self.create_circle_marker(radius=self.sld_distance.value)
				)

				self.page.update()

			else:
				logger.warning("Location permissions are not granted. Asking for permissions...")
				self.page.open(self.dlg_request_location_permission)

		except Exception as e:
			logger.error(f"Error applying filters: {e}")
			self.dlg_error.title.value = "Error al aplicar filtros"
			self.dlg_error.content.value = (
				"Ocurrió un error al aplicar los filtros. "
				"Favor de intentarlo de nuevo más tarde."
			)
			self.page.open(self.dlg_error)

	def clean_filters(self, _: ft.ControlEvent) -> None:
		logger.info("Cleaning filters...")
		self.drd_classification.value = ""
		self.sld_distance.value = 7
		self.page.update()

	def handle_map_click(self, event: map.MapTapEvent) -> None:
		clicked_lat: float = event.coordinates.latitude
		clicked_lon: float = event.coordinates.longitude

		# Buscar el marcador más cercano al clic
		for marker in self.marker_layer.markers:
			marker_lat: float = marker.coordinates.latitude
			marker_lon: float = marker.coordinates.longitude
			marker_coordinates: tuple = (marker_lat, marker_lon)
			clicked_distance: float = geodesic((clicked_lat, clicked_lon), marker_coordinates).kilometers

			# Si la distancia es menor a un umbral (por ejemplo, 300 metros)
			if clicked_distance <= 0.05: # 50 metros
				place_data: dict = marker.data
				self.page.session.set(key="place_id", value=place_data["id"])

				self.dlg_place_info.title.value = place_data["name"]
				self.dlg_place_info.content.value = (
					f"Clasificación: {place_data['classification']}\n\n"
					f"Dirección: {place_data['address']}\n\n"
					f"Distancia: {place_data['distancia']:.2f} km"
				)
				self.page.open(self.dlg_place_info)

	def handle_map_event(self, event: map.MapEvent) -> None:
		if str(event.source) == "MapEventSource.SCROLL_WHEEL":
			if event.zoom >= 15 and self.markers_names_are_hidden:
				logger.info("Showing markers names...")
				for marker in self.marker_layer.markers:
					marker.content.controls[-1].visible = True
				self.markers_names_are_hidden = False

			if event.zoom < 15 and not self.markers_names_are_hidden:
				logger.info("Hiding markers names...")
				for marker in self.marker_layer.markers:
					marker.content.controls[-1].visible = False
				self.markers_names_are_hidden = True

			self.page.update()

	def handle_accept_location_permission(self, _: ft.ControlEvent) -> None:
		if request_location_permissions(self.gl, logger):
			logger.info("Location permissions granted. Getting current coordinates. Opening location permissions failed dialog...")
			self.page.open(self.dlg_location_permissions_succeded)

		else:
			logger.warning("Location permissions denied. Opening location permissions failed dialog...")
			self.page.open(self.dlg_location_permissions_failed)
