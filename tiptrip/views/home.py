import flet as ft
from logging import Logger, getLogger

from requests import get, post, Response
from requests.exceptions import ConnectTimeout

from components.bars import *
from resources.config import *
from resources.functions import *
from components.splash import Splash
from components.place_card import PlaceCard
from resources.styles import txt_messages_style


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class HomeView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page

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

		# Filters components
		self.txt_place_searcher: ft.TextField = ft.TextField(
			prefix_icon=ft.Icons.SEARCH,
			label="Busca un sitio turístico",
			on_change=self.search_place,
			**txt_messages_style
		)
		self.drd_municipality: ft.Dropdown = ft.Dropdown(
			label="Filtrar por delegación",
			value=self.page.session.get("drd_municipality_value"),
			options=[
				ft.dropdown.Option(municipality)
				for municipality in MUNICIPALITIES
			]
		)
		self.drd_classification: ft.Dropdown = ft.Dropdown(
			label="Filtrar por clasificación",
			value=self.page.session.get("drd_classification_value"),
			options=[
				ft.dropdown.Option(classification)
				for classification in CLASSIFICATIONS
			]
		)
		self.chk_distance: ft.Checkbox = ft.Checkbox(
			label="Filtrar por cercanía",
			value=self.page.session.get("chk_distance_value"),
			data=ft.PermissionType.LOCATION,
			on_change=self.activate_or_desactivate_distance_filter
		)
		self.sld_distance: ft.Slider = ft.Slider(
			min=1,
			max=15,
			value=self.page.session.get("sld_value"),
			divisions=5,
			label="{value} km",
			disabled=(
				False
				if self.page.session.get("chk_distance_value")
				else True
			)
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
					ft.Container(
						margin=ft.margin.only(left=7),
						content=ft.Text(
							value="Seleccionar distancia:",
							color=(
								ft.Colors.WHITE
								if self.chk_distance.value
								else ft.Colors.GREY_400
							)
						)
					),
					ft.Container(content=self.sld_distance),
					ft.Container(
						content=ft.TextButton(
							text="Eliminar filtros",
							data=ft.PermissionType.LOCATION,
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
					data=ft.PermissionType.LOCATION,
					on_click=self.apply_filters
				)
			],
			on_dismiss=lambda _: self.page.close(self.dlg_sites_filter)
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

		# Places and pagination variables
		self.page.session.set(
			key="places_data",
			value=(
				self.get_places(distance=100)
				if self.page.session.get("places_data") is None
				else self.page.session.get("places_data")
			)
		)

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
				self.page.session.get("places_data")
				if isinstance(self.page.session.get("places_data"), ft.Container)
				else self.page.session.get("places_data")[self.page_start_index:self.page_end_index]
			)
		)

		self.total_items: int = len(self.page.session.get("places_data"))
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
					)
				]
			)
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
			route='/',
			bgcolor=ft.Colors.WHITE,
			padding=ft.padding.all(value=0.0),
			spacing=0,
			floating_action_button=ft.FloatingActionButton(
				icon=ft.Icons.LOCATION_ON,
				bgcolor=SECONDARY_COLOR,
				foreground_color=ft.Colors.WHITE,
				shape=ft.CircleBorder(),
				data=ft.PermissionType.LOCATION,
				on_click=self.check_if_open_map
			),
			floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_DOCKED,
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
						color=ft.Colors.GREY_800
					)
				),
				ft.Container(
					expand=True,
					width=self.page.width,
					content=ft.Stack(
						controls=[
							ft.Container(
								content=ft.Column(
									controls=[
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
														padding=ft.padding.symmetric(horizontal=(SPACING / 2)),
														border_radius=ft.border_radius.all(value=RADIUS),
														shadow=ft.BoxShadow(
															blur_radius=(BLUR / 2),
															offset=ft.Offset(0, 2),
															color=ft.Colors.GREY
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
																		bgcolor=ft.Colors.WHITE,
																		radius=SPACING,
																		content=ft.Icon(
																			name=ft.Icons.FILTER_LIST,
																			color=ft.Colors.BLACK
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
										)
									]
								)
							),
							self.cont_splash
						]
					)
				)
			],
			bottom_appbar=BottomBar(page=self.page, logger=logger, current_route='/')
		)

	def get_places(
		self,
		distance: int,
		classification: str = None,
		municipality: str = None
	) -> list:

		logger.info("Checking if user is inside CDMX coordinates...")
		if not self.page.session.get("is_inside_cdmx"):
			logger.warning("User's location is outside CDMX coordinates. Deactivating distance filter...")

			logger.info("Continuing without distance filter...")
			distance = None

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
					"municipality": municipality,
					"distance": distance,
					"current_latitude": self.page.session.get("current_latitude"),
					"current_longitude": self.page.session.get("current_longitude")
				}
			)

		except ConnectTimeout:
			logger.error("Connection timeout while getting favorite places")
			self.dlg_error.title = ft.Text("Error de conexión a internet")
			self.dlg_error.content = ft.Text(
				"No se pudo obtener información sobre los sitios turísticos. "
				"Favor de revisar su conexión a internet e intentarlo de nuevo más tarde."
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
				return [
					ft.Container(
						alignment=ft.alignment.center,
						content=ft.Text(
							value=(
								"Ocurrió un error al obtener la información de "
								"los sitios turísticos."
							),
							color=ft.Colors.BLACK,
							size=30
						)
					)
				]

		logger.info(f"Evaluating response with status {response.status_code}...")
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
					image_name=get_placecard_image(place["info"]["name"]),
					is_favorite=place["is_favorite"],
					punctuation=place["info"]["punctuation"],
					distance=place["distance"] if "distance" in place else None
				)
				for place in places
			]

		elif response.status_code == 204:
			logger.info(f"Places endpoint response received: {response.json()}")
			return [
				ft.Container(
					alignment=ft.alignment.center,
					content=ft.Text(
						value=(
							"No se encontró ningún sitio turístico con "
							"los filtros seleccionados."
						),
						color=ft.Colors.BLACK,
						size=30
					)
				)
			]

		else:
			logger.info(f"Places endpoint response received: {response.json()}")
			return [
				ft.Container(
					alignment=ft.alignment.center,
					content=ft.Text(
						value=(
							"Ocurrió un error al obtener la información de "
							"los sitios turísticos."
						),
						color=ft.Colors.BLACK,
						size=30
					)
				)
			]

	def update_pagination_data(self, items: list) -> None:
		logger.info("Updating pagination data...")
		self.current_page = 0
		self.total_items = len(items)
		self.total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
		self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"

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

	def set_page_indexes(self) -> None:
		logger.info("Setting page indexes...")
		self.page_start_index = self.current_page * self.items_per_page
		self.page_end_index = self.page_start_index + self.items_per_page
		self.lv_places_list.controls = (
			self.page.session.get("places_data")
			if len(self.page.session.get("places_data")) == 1 and isinstance(self.page.session.get("places_data")[0], ft.Container)
			else self.page.session.get("places_data")[self.page_start_index:self.page_end_index]
		)

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

	def previous_page(self, _: ft.ControlEvent) -> None:
		logger.info(f"Going to previous page...")
		if self.current_page > 0:
			self.current_page -= 1
		else:
			self.current_page = self.total_pages - 1

		self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
		self.set_page_indexes()

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

	def next_page(self, _: ft.ControlEvent) -> None:
		logger.info(f"Going to next page...")
		if self.current_page < self.total_pages - 1:
			self.current_page += 1
		else:
			self.current_page = 0

		self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
		self.set_page_indexes()

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

	def search_place(self, _: ft.ControlEvent) -> None:
		if self.txt_place_searcher.value == "":
			logger.info("Cleaning 'searching place' filter...")
			self.lv_places_list.controls = self.page.session.get("places_data")[0:self.items_per_page]
			self.update_pagination_data(self.page.session.get("places_data"))
		else:
			value: str = self.txt_place_searcher.value.lower()
			logger.info(f"Searching place by: {value}")
			items: list = [
				place for place in self.page.session.get("places_data") if value in
				# Searching in the structure of the PlaceCard component in place_card.py
				place.content.controls[0].content.controls[0].value.lower()
			]
			self.lv_places_list.controls = items[0:self.items_per_page]
			self.update_pagination_data(items)

	def activate_or_desactivate_distance_filter(self, event: ft.ControlEvent) -> None:
		try:
			self.page.close(self.dlg_sites_filter)
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.close(self.dlg_sites_filter)

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

		# Case when the distance filter was activated
		if not self.chk_distance.value:
			logger.info("Deactivating distance filter...")
			self.sld_distance.disabled = True

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

			logger.info("Storing new distance filter value and coordinates in session...")
			self.page.session.set(key="chk_distance_value", value=False)
			self.page.session.set(key="current_latitude", value=None)
			self.page.session.set(key="current_longitude", value=None)

		# Case when the distance filter was NOT activated
		else:
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

					logger.info("Verifying if user's location is inside CDMX coordinates...")
					if is_inside_cdmx((self.page.session.get("current_latitude"), self.page.session.get("current_longitude"))):
						logger.info("User's location is inside CDMX coordinates. Activating distance filter...")
						self.sld_distance.disabled = False
						self.chk_distance.value = True

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

						logger.info("Storing new distance filter values in session...")
						self.page.session.set(key="is_inside_cdmx", value=True)
						self.page.session.set(key="chk_distance_value", value=True)

					else:
						logger.warning("User's location is outside CDMX coordinates. Disabling distance filter...")
						self.page.session.set(key="is_inside_cdmx", value=False)
						self.page.session.set(key="chk_distance_value", value=False)
						self.chk_distance.value = False
						logger.info("Opening outside CDMX location dialog...")
						self.dlg_error.title = ft.Text(value="Ubicación fuera de CDMX")
						self.dlg_error.content = ft.Text(
							value=(
								"Tu ubicación actual se encuentra fuera de los límites de la Ciudad de México, "
								"por lo que no se puede aplicar el filtro de cercanía."
							)
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
						"por lo que no se puede activar el filtro de cercanía."
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

			else:
				logger.warning("Location permissions are not granted...")
				logger.info("Hidding loading splash screen...")
				self.cont_splash.visible = False
				self.splash.visible = False

				logger.info("Deactivating distance filter...")
				self.page.session.set(key="is_inside_cdmx", value=False)
				self.page.session.set(key="chk_distance_value", value=False)
				self.chk_distance.value = False

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

				logger.info("Opening location permissions dialog...")
				self.dlg_error.title = ft.Text("Permisos de ubicación")
				self.dlg_error.content = ft.Text(
					"No se han otorgado los permisos de ubicación, "
					"por lo que no se puede activar el filtro de cercanía."
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

			logger.info("Applying filters...")
			try:
				self.page.close(self.dlg_sites_filter)
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.close(self.dlg_sites_filter)

			logger.info("Storing new filters values in session...")
			self.page.session.set(key="drd_classification_value", value=self.drd_classification.value)
			self.page.session.set(key="drd_municipality_value", value=self.drd_municipality.value)
			self.page.session.set(key="sld_value", value=self.sld_distance.value)

			logger.info("Checking location permissions...")
			permission: ft.PermissionStatus = self.ph.request_permission(event.control.data, wait_timeout=60)
			logger.info(f"Location permissions status: {permission}")
			if permission == ft.PermissionStatus.GRANTED:
				try:
					logger.info("Location permissions granted. Getting current coordinates...")
					current_position: ft.GeolocatorPosition = self.gl.get_current_position()
					self.page.session.set(key="current_latitude", value=current_position.latitude)
					self.page.session.set(key="current_longitude", value=current_position.longitude)
					logger.info(f"Got current coordinates: ({current_position.latitude}, {current_position.longitude})")
				except Exception as e:
					logger.error(f"Error getting current coordinates: {e}")
					self.page.session.set(key="current_latitude", value=None)
					self.page.session.set(key="current_longitude", value=None)

			else:
				logger.warning("Location permissions are not granted. Continuing without distance filter...")
				self.page.session.set(key="current_latitude", value=None)
				self.page.session.set(key="current_longitude", value=None)

			logger.info("Getting places info...")
			self.page.session.set(
				key="places_data",
				value=self.get_places(
					distance=self.page.session.get("sld_value"),
					classification=(
						self.page.session.get("drd_classification_value")
						if self.page.session.get("drd_classification_value") != "Seleccionar todas"
						else None
					),
					municipality=(
						self.page.session.get("drd_municipality_value")
						if self.page.session.get("drd_municipality_value") != "Seleccionar todas"
						else None
					)
				)
			)

			logger.info("Updating view with new info...")
			self.set_page_indexes()
			self.update_pagination_data(self.page.session.get("places_data"))

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

			logger.error(f"Error applying filters: {e}")
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

			logger.info("Cleaning filters process started...")
			try:
				self.page.close(self.dlg_sites_filter)
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.close(self.dlg_sites_filter)
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

			logger.info("Storing new clean filters values in session...")
			self.page.session.set(key="drd_classification_value", value="Seleccionar todas")
			self.page.session.set(key="drd_municipality_value", value="Seleccionar todas")
			self.page.session.set(key="sld_value", value=7)

			logger.info("Cleaning components values...")
			self.drd_classification.value = "Seleccionar todas"
			self.drd_municipality.value = "Seleccionar todas"
			self.sld_distance.value = 7
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
				try:
					logger.info("Location permissions granted. Getting current coordinates")
					current_position: ft.GeolocatorPosition = self.gl.get_current_position()
					self.page.session.set(key="current_latitude", value=current_position.latitude)
					self.page.session.set(key="current_longitude", value=current_position.longitude)
					logger.info(f"Got current coordinates: ({current_position.latitude}, {current_position.longitude})")
				except Exception as e:
					logger.error(f"Error getting current coordinates: {e}")
					self.page.session.set(key="current_latitude", value=None)
					self.page.session.set(key="current_longitude", value=None)
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
				logger.warning("Location permissions are not granted. Continuing without distance filter...")
				self.page.session.set(key="current_latitude", value=None)
				self.page.session.set(key="current_longitude", value=None)

			logger.info("Getting places info...")
			self.page.session.set(
				key="places_data",
				value=self.get_places(
					distance=100,
					classification=(
						self.page.session.get("drd_classification_value")
						if self.page.session.get("drd_classification_value") != "Seleccionar todas"
						else None
					),
					municipality=(
						self.page.session.get("drd_municipality_value")
						if self.page.session.get("drd_municipality_value") != "Seleccionar todas"
						else None
					)
				)
			)

			logger.info("Updating view with new info...")
			self.set_page_indexes()
			self.update_pagination_data(self.page.session.get("places_data"))

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

			logger.error(f"Error cleaning filters: {e}")
			self.dlg_error.title.value = "Error al limpiar filtros"
			self.dlg_error.content.value = (
				"Ocurrió un error al limpiar los filtros. "
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

	def check_if_open_map(self, event: ft.ControlEvent) -> None:
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
			logger.info("Location permissions are granted...")
			try:
				go_to_view(self.page, logger=logger, route="/map")
			except Exception as e:
				logger.error(f"Error: {e}")
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)
				go_to_view(self.page, logger=logger, route="/map")

			logger.info("Hidding loading splash screen...")
			self.cont_splash.visible = False
			self.splash.visible = False
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)
				self.page.update()

		else:
			logger.warning("Location permissions are not granted...")
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
				"Para acceder al mapa interactivo, "
				"necesitamos que permitas el acceso a tu ubicación."
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
