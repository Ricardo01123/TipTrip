import flet as ft
import flet.map as map
from typing import Optional
from geopy.distance import geodesic
from logging import Logger, getLogger

from requests import get, post, Response
from requests.exceptions import ConnectTimeout

from resources.config import *
from resources.functions import *
from components.bars import TopBar
from components.splash import Splash
from resources.config import PROJECT_NAME


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class MapView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page
		self.markers_names_are_hidden: bool = True
		self.markers_names_umbral: int = 15

		# Custom components
		self.ph: ft.PermissionHandler = ft.PermissionHandler()
		page.overlay.append(self.ph)

		self.gl: ft.Geolocator = ft.Geolocator(
			location_settings=ft.GeolocatorSettings(
				accuracy=ft.GeolocatorPositionAccuracy.BEST
			),
			on_error=lambda _: post(
				url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
				headers={"Content-Type": "application/json"},
				json={
					"user_id": self.page.session.get("id"),
					"file": encode_logfile()
				}
			)
		)
		self.page.overlay.append(self.gl)

		# Map components
		self.page.session.set(
			key="map_places_data",
			value=(
				self.get_places(distance=100)
				if self.page.session.get("map_places_data") is None
				else self.page.session.get("map_places_data")
			)
		)
		self.circle_layer = map.CircleLayer(
			circles=[
				self.create_circle_marker(radius=self.page.session.get("map_sld_value"))
			]
		)
		self.marker_layer = map.MarkerLayer(
			markers=[
				*self.create_places_markers(self.page.session.get("map_places_data")),
				self.create_user_marker()
			]
		)
		self.map = map.Map(
			expand=True,
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
			on_event=self.handle_map_event,
			layers=[
				map.TileLayer(
					url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
					on_image_error=lambda error: logger.error(f"TileLayer (MapLayer) error: {error}"),
				),
				map.RichAttribution(
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
			value=self.page.session.get("map_drd_value"),
			options=[
				ft.dropdown.Option(classification)
				for classification in CLASSIFICATIONS
			]
		)
		self.sld_distance: ft.Slider = ft.Slider(
			min=1,
			max=15,
			value=self.page.session.get("map_sld_value"),
			divisions=5,
			label="{value} km",
			active_color=SECONDARY_COLOR,
			thumb_color=SECONDARY_COLOR
		)
		self.ext_settings: ft.ExpansionTile = ft.ExpansionTile(
			trailing=ft.Icon(
				name=ft.Icons.KEYBOARD_ARROW_DOWN,
				color=ft.Colors.BLACK,
				size=22
			),
			title=ft.Text(
				value="Filtrar sitios turísticos",
				color=ft.Colors.BLACK,
				size=16
			),
			tile_padding=ft.padding.symmetric(horizontal=SPACING),
			controls=[
				ft.Container(
					padding=ft.padding.symmetric(horizontal=SPACING),
					content=self.drd_classification,
				),
				ft.Container(
					bgcolor=ft.Colors.TRANSPARENT,
					padding=ft.padding.only(
						top=SPACING,
						left=SPACING,
						right=SPACING,
						bottom=0
					),
					alignment=ft.alignment.center_left,
					content=ft.Text(
						value="Distancia de mí:",
						color=ft.Colors.BLACK,
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
								color=ft.Colors.WHITE,
								text="Limpiar filtros",
								data=ft.PermissionType.LOCATION,
								on_click=self.clean_filters,
							),
							ft.ElevatedButton(
								bgcolor=SECONDARY_COLOR,
								color=ft.Colors.WHITE,
								text="Aplicar filtros",
								data=ft.PermissionType.LOCATION,
								on_click=self.apply_filters,
							)
						]
					)
				)
			]
		)

		# Splash components
		self.splash = Splash(page=self.page)
		self.splash.visible = False
		self.page.overlay.append(self.splash)
		self.cont_splash = ft.Container(
			expand=True,
			width=self.page.width,
			bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
			content=None,
			visible=False
		)

		# View native attributes
		super().__init__(
			route = "/map",
			bgcolor=ft.Colors.WHITE,
			padding=ft.padding.all(value=0.0),
			spacing=0,
			floating_action_button=ft.FloatingActionButton(
				icon=ft.Icons.MY_LOCATION,
				bgcolor=MAIN_COLOR,
				foreground_color=ft.Colors.WHITE,
				shape=ft.CircleBorder(),
				data=ft.PermissionType.LOCATION,
				on_click=self.center_user
			),
			floating_action_button_location=ft.FloatingActionButtonLocation.MINI_END_FLOAT,
			controls=[
				TopBar(page=self.page, leading=True, logger=logger),
				ft.Container(
					width=self.page.width,
					bgcolor=MAIN_COLOR,
					shadow=ft.BoxShadow(
						blur_radius=BLUR,
						color=ft.Colors.GREY_800
					),
					content=self.ext_settings
				),
				ft.Container(
					expand=True,
					width=self.page.width,
					content=ft.Stack(
						controls=[
							ft.Container(content=self.map),
							self.cont_splash
						]
					)
				)
			]
		)

	def get_places(self, distance: int, classification: str = None) -> Optional[list]:
		logger.info("Getting places data...")
		try:
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

		except ConnectTimeout:
			logger.error("Connection timeout while deleting account")
			self.dlg_error.title = ft.Text(value="Error de conexión a internet")
			self.dlg_error.content = ft.Text(
				value=(
					"No se pudo obtener información sobre los sitios turísticos. "
					"Favor de revisar su conexión a internet e intentarlo de nuevo más tarde."
				)
			)

			try:
				self.page.open(self.dlg_error)

			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.open(self.dlg_error)
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

			finally:
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)
				return None

		logger.info("Evaluating response...")
		if response.status_code == 200:
			places: list = response.json()["places"]
			logger.info(f"Obtained a total of {len(places)} places...")
			return places

		elif response.status_code == 204:
			logger.warning("No places found...")
			return []

		else:
			logger.error(f"Places endpoint response received {response.status_code}: {response.json()}")
			return None

	def create_user_marker(self) -> map.Marker:
		logger.info("Creating user marker...")
		return map.Marker(
			content=ft.Row(
				controls=[
					ft.Icon(
						name=ft.Icons.PERSON_PIN_CIRCLE_ROUNDED,
						color=SECONDARY_COLOR,
						size=30
					),
					ft.Text(
						value="Yo",
						size=16,
						color=ft.Colors.BLACK,
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

	def create_circle_marker(self, radius: int) -> map.CircleMarker:
		logger.info("Creating circle marker...")
		return map.CircleMarker(
			coordinates=map.MapLatitudeLongitude(
				self.page.session.get("current_latitude"),
				self.page.session.get("current_longitude")
			),
			use_radius_in_meter=True,
			radius=(radius * 1000),
			color=ft.Colors.with_opacity(0.07, ft.Colors.BLUE),
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
							name=ft.Icons.LOCATION_ON_ROUNDED,
							color=ft.Colors.RED,
							size=30
						),
						ft.Text(
							value=place["info"]["name"],
							size=16,
							color=ft.Colors.BLACK,
							weight=ft.FontWeight.BOLD,
							visible=False
						)
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
					"distance": place["distance"]
				}
			) for place in items
		]

	def center_user(self, event: ft.ControlEvent) -> None:
		try:
			logger.info("Showing loading splash screen...")
			self.cont_splash.visible = True
			self.splash.visible = True
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

			logger.info("Checking location permissions...")
			permission: ft.PermissionStatus = self.ph.request_permission(event.control.data, wait_timeout=60)
			logger.info(f"Location permissions status: {permission}")
			if permission == ft.PermissionStatus.GRANTED:
				logger.info("Location permissions granted. Getting current coordinates")
				try:
					current_position: ft.GeolocatorPosition = self.gl.get_current_position()
					self.page.session.set(key="current_latitude", value=current_position.latitude)
					self.page.session.set(key="current_longitude", value=current_position.longitude)
					logger.info(f"Got current coordinates: ({current_position.latitude}, {current_position.longitude})")

					logger.info("Centering map on user coordinates...")
					if self.marker_layer.markers != []:
						self.marker_layer.markers.pop()
					self.marker_layer.markers.append(self.create_user_marker())

					logger.info("Adding circle distance radius marker...")
					if self.circle_layer.circles != []:
						self.circle_layer.circles.pop()
					self.circle_layer.circles.append(
						self.create_circle_marker(radius=self.page.session.get("map_sld_value"))
					)

					logger.info("Moving to user coordinates...")
					self.map.move_to(
						destination=map.MapLatitudeLongitude(
							self.page.session.get("current_latitude"),
							self.page.session.get("current_longitude")
						),
						zoom=13
					)

					logger.info("Reseting map rotation...")
					self.map.reset_rotation()

					logger.info("Hidding loading splash screen...")
					self.cont_splash.visible = False
					self.splash.visible = False
					try:
						self.page.update()
					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.update()
						#! COMMENT
						post(
							url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
							headers={"Content-Type": "application/json"},
							json={
								"user_id": self.page.session.get("id"),
								"file": encode_logfile()
							}
						)

				except Exception as e:
					logger.warning(f"Error getting current coordinates: {e}")
					logger.info("Hidding loading splash screen...")
					self.cont_splash.visible = False
					self.splash.visible = False
					try:
						self.page.update()
					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.update()
						#! COMMENT
						post(
							url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
							headers={"Content-Type": "application/json"},
							json={
								"user_id": self.page.session.get("id"),
								"file": encode_logfile()
							}
						)

					self.dlg_error.title = ft.Text("Permisos de ubicación")
					self.dlg_error.content = ft.Text(
						"No se han otorgado los permisos de ubicación, "
						"por lo que no se puede centrar el mapa en la ubicación actual."
					)
					try:
						self.page.open(self.dlg_error)
					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.open(self.dlg_error)
						#! COMMENT
						post(
							url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
							headers={"Content-Type": "application/json"},
							json={
								"user_id": self.page.session.get("id"),
								"file": encode_logfile()
							}
						)

					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

			else:
				logger.info("Hidding loading splash screen...")
				self.cont_splash.visible = False
				self.splash.visible = False
				try:
					self.page.update()
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.update()
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

				self.dlg_error.title = ft.Text("Permisos de ubicación")
				self.dlg_error.content = ft.Text(
					"No se han otorgado los permisos de ubicación, "
					"por lo que no se puede centrar el mapa en la ubicación actual."
				)
				try:
					self.page.open(self.dlg_error)
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.open(self.dlg_error)
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

		except Exception as e:
			logger.info("Hidding loading splash screen...")
			self.cont_splash.visible = False
			self.splash.visible = False

			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

			logger.error(f"Error centering user on map: {e}")
			self.dlg_error.title.value = "Error al centrar usuario"
			self.dlg_error.content.value = (
				"Ocurrió un error al centrar el mapa en tu ubicación. "
				"Favor de intentarlo de nuevo más tarde."
			)

			try:
				self.page.open(self.dlg_error)
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.open(self.dlg_error)
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

	def apply_filters(self, event: ft.ControlEvent) -> None:
		try:
			logger.info("Showing loading splash screen...")
			self.cont_splash.visible = True
			self.splash.visible = True

			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

			logger.info("Checking location permissions...")
			permission: ft.PermissionStatus = self.ph.request_permission(event.control.data, wait_timeout=60)
			logger.info(f"Location permissions status: {permission}")
			if permission == ft.PermissionStatus.GRANTED:
				logger.info("Location permissions granted. Storing new filters values in session...")
				self.page.session.set(key="map_sld_value", value=self.sld_distance.value)
				self.page.session.set(key="map_drd_value", value=self.drd_classification.value)

				self.page.session.set(
					key="map_places_data",
					value=self.get_places(
						distance=self.page.session.get("map_sld_value"),
						classification=(
							self.page.session.get("map_drd_value")
							if self.page.session.get("map_drd_value") != "Seleccionar todas" else None
						)
					)
				)
				if self.page.session.get("map_places_data") is not None or self.page.session.get("map_places_data") == []:
					if self.page.session.get("map_places_data") == []:
						logger.warning("No places found")
						self.dlg_error.title.value = "Sin resultados"
						self.dlg_error.content.value = "No se encontró ningún lugar turístico con los filtros aplicados."

						logger.info("Hidding loading splash screen...")
						self.cont_splash.visible = False
						self.splash.visible = False

						try:
							self.page.update()
						except Exception as e:
							logger.error(f"Error: {e}")
							self.page.update()
							#! COMMENT
							post(
								url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
								headers={"Content-Type": "application/json"},
								json={
									"user_id": self.page.session.get("id"),
									"file": encode_logfile()
								}
							)

						try:
							self.page.open(self.dlg_error)
						except Exception as e:
							logger.error(f"Error: {e}")
							self.page.open(self.dlg_error)
							#! COMMENT
							post(
								url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
								headers={"Content-Type": "application/json"},
								json={
									"user_id": self.page.session.get("id"),
									"file": encode_logfile()
								}
							)
						finally:
							return

					else:
						logger.info("Cleaning previous markers...")
						self.marker_layer.markers = []

						logger.info("Creating new markers...")
						new_places: Optional[list] = self.create_places_markers(self.page.session.get("map_places_data"))
						self.marker_layer.markers = [*new_places]

				else:
					logger.error("Error getting nearby places")
					self.dlg_error.title.value = "Error al aplicar filtros"
					self.dlg_error.content.value = (
						"Ocurrió un error al aplicar los filtros. "
						"Favor de intentarlo de nuevo más tarde."
					)

					logger.info("Hidding loading splash screen...")
					self.cont_splash.visible = False
					self.splash.visible = False
					try:
						self.page.update()
					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.update()
						#! COMMENT
						post(
							url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
							headers={"Content-Type": "application/json"},
							json={
								"user_id": self.page.session.get("id"),
								"file": encode_logfile()
							}
						)

					try:
						self.page.open(self.dlg_error)
					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.open(self.dlg_error)
						#! COMMENT
						post(
							url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
							headers={"Content-Type": "application/json"},
							json={
								"user_id": self.page.session.get("id"),
								"file": encode_logfile()
							}
						)
					finally:
						return

				logger.info("Getting current coordinates...")
				current_position: ft.GeolocatorPosition = self.gl.get_current_position()
				self.page.session.set(key="current_latitude", value=current_position.latitude)
				self.page.session.set(key="current_longitude", value=current_position.longitude)
				logger.info(f"Got current coordinates: ({current_position.latitude}, {current_position.longitude})")

				logger.info("Centering map on user coordinates...")
				if self.marker_layer.markers != []:
					self.marker_layer.markers.pop()
				self.marker_layer.markers.append(self.create_user_marker())

				logger.info("Adding circle distance radius marker...")
				if self.circle_layer.circles != []:
					self.circle_layer.circles.pop()
				self.circle_layer.circles.append(
					self.create_circle_marker(radius=self.page.session.get("map_sld_value"))
				)

				logger.info("Moving to user coordinates...")
				self.map.move_to(
					destination=map.MapLatitudeLongitude(
						self.page.session.get("current_latitude"),
						self.page.session.get("current_longitude")
					),
					zoom=13
				)

				logger.info("Hidding loading splash screen...")
				self.cont_splash.visible = False
				self.splash.visible = False
				try:
					self.page.update()
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.update()
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

			else:
				logger.warning("Location permissions are not granted")
				logger.info("Hidding loading splash screen...")
				self.cont_splash.visible = False
				self.splash.visible = False
				try:
					self.page.update()
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.update()
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

				self.dlg_error.title.value = "Permisos de ubicación"
				self.dlg_error.content.value = (
					"No se han otorgado los permisos de ubicación, "
					"por lo que no se pueden aplicar los filtros."
				)

				try:
					self.page.open(self.dlg_error)
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.open(self.dlg_error)
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

		except Exception as e:
			logger.error(f"Error applying filters: {e}")
			logger.info("Hidding loading splash screen...")
			self.cont_splash.visible = False
			self.splash.visible = False
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()

			self.dlg_error.title.value = "Error al aplicar filtros"
			self.dlg_error.content.value = (
				"Ocurrió un error al aplicar los filtros. "
				"Favor de intentarlo de nuevo más tarde."
			)

			try:
				self.page.open(self.dlg_error)
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.open(self.dlg_error)

			#! COMMENT
			post(
				url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
				headers={"Content-Type": "application/json"},
				json={
					"user_id": self.page.session.get("id"),
					"file": encode_logfile()
				}
			)

	def clean_filters(self, event: ft.ControlEvent) -> None:
		try:
			logger.info("Showing loading splash screen...")
			self.cont_splash.visible = True
			self.splash.visible = True
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

			logger.info("Checking location permissions...")
			permission: ft.PermissionStatus = self.ph.request_permission(event.control.data, wait_timeout=60)
			logger.info(f"Location permissions status: {permission}")
			if permission == ft.PermissionStatus.GRANTED:
				logger.info("Location permissions granted. Cleaning filters...")
				self.page.session.set(key="map_sld_value", value=7)
				self.page.session.set(key="map_drd_value", value="Seleccionar todas")
				self.sld_distance.value = 7
				self.drd_classification.value = "map_drd_value"

				self.page.session.set(
					key="map_places_data",
					value=self.get_places(
						distance=100,
						classification=(
							self.page.session.get("map_drd_value")
							if self.page.session.get("map_drd_value") != "map_drd_value"
							else None
						)
					)
				)
				if self.page.session.get("map_places_data") is not None or self.page.session.get("map_places_data") == []:
					if self.page.session.get("map_places_data") == []:
						logger.warning("No places found")
						self.dlg_error.title.value = "Sin resultados"
						self.dlg_error.content.value = "No se encontró ningún lugar turístico con los filtros aplicados."

						logger.info("Hidding loading splash screen...")
						self.cont_splash.visible = False
						self.splash.visible = False
						try:
							self.page.update()
						except Exception as e:
							logger.error(f"Error: {e}")
							self.page.update()
							#! COMMENT
							post(
								url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
								headers={"Content-Type": "application/json"},
								json={
									"user_id": self.page.session.get("id"),
									"file": encode_logfile()
								}
							)

						try:
							self.page.open(self.dlg_error)
						except Exception as e:
							logger.error(f"Error: {e}")
							self.page.open(self.dlg_error)
							#! COMMENT
							post(
								url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
								headers={"Content-Type": "application/json"},
								json={
									"user_id": self.page.session.get("id"),
									"file": encode_logfile()
								}
							)
						finally:
							return

					else:
						logger.info("Cleaning previous markers...")
						self.marker_layer.markers = []

						logger.info("Creating new markers...")
						new_places: Optional[list] = self.create_places_markers(self.page.session.get("map_places_data"))
						self.marker_layer.markers = [*new_places]

				else:
					logger.error("Error getting nearby places")
					self.dlg_error.title.value = "Error al aplicar filtros"
					self.dlg_error.content.value = (
						"Ocurrió un error al aplicar los filtros. "
						"Favor de intentarlo de nuevo más tarde."
					)

					logger.info("Hidding loading splash screen...")
					self.cont_splash.visible = False
					self.splash.visible = False
					try:
						self.page.update()
					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.update()
						#! COMMENT
						post(
							url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
							headers={"Content-Type": "application/json"},
							json={
								"user_id": self.page.session.get("id"),
								"file": encode_logfile()
							}
						)

					try:
						self.page.open(self.dlg_error)
					except Exception as e:
						logger.error(f"Error: {e}")
						self.page.open(self.dlg_error)
						#! COMMENT
						post(
							url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
							headers={"Content-Type": "application/json"},
							json={
								"user_id": self.page.session.get("id"),
								"file": encode_logfile()
							}
						)
					finally:
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
					self.create_circle_marker(radius=self.page.session.get("map_sld_value"))
				)

				logger.info("Hidding loading splash screen...")
				self.cont_splash.visible = False
				self.splash.visible = False
				try:
					self.page.update()
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.update()
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

			else:
				logger.warning("Location permissions are not granted. Asking for permissions...")

				logger.info("Hidding loading splash screen...")
				self.cont_splash.visible = False
				self.splash.visible = False
				try:
					self.page.update()
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.update()
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

				self.dlg_error.title.value = "Permisos de ubicación"
				self.dlg_error.content.value = (
					"No se han otorgado los permisos de ubicación, "
					"por lo que no se pueden aplicar los filtros."
				)

				try:
					self.page.open(self.dlg_error)
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.open(self.dlg_error)
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

		except Exception as e:
			logger.error(f"Error applying filters: {e}")
			logger.info("Hidding loading splash screen...")
			self.cont_splash.visible = False
			self.splash.visible = False
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

			self.dlg_error.title.value = "Error al aplicar filtros"
			self.dlg_error.content.value = (
				"Ocurrió un error al aplicar los filtros. "
				"Favor de intentarlo de nuevo más tarde."
			)

			try:
				self.page.open(self.dlg_error)
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.open(self.dlg_error)
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

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
					(
						f"Clasificación: {place_data['classification']}\n\n"
						f"Dirección: {place_data['address']}\n\n"
						f"Distancia: {place_data['distance']:.2f} km"
					)
					if place_data["distance"] is not None else
					(
						f"Clasificación: {place_data['classification']}\n\n"
						f"Dirección: {place_data['address']}"
					)
				)
				try:
					self.page.open(self.dlg_place_info)
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.open(self.dlg_place_info)
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

	def handle_map_event(self, event: map.MapEvent) -> None:
		logger.info(f"Map event: {event}")
		logger.info(f"Map event source: {event.source}")
		if str(event.source) == "MapEventSource.SCROLL_WHEEL":
			if event.zoom >= self.markers_names_umbral and self.markers_names_are_hidden:
				logger.info("Showing markers names...")
				for marker in self.marker_layer.markers:
					marker.content.controls[-1].visible = True
				self.markers_names_are_hidden = False

			if event.zoom < self.markers_names_umbral and not self.markers_names_are_hidden:
				logger.info("Hiding markers names...")
				for marker in self.marker_layer.markers:
					marker.content.controls[-1].visible = False
				self.markers_names_are_hidden = True

			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)
