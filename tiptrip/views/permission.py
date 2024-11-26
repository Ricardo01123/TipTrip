import flet as ft
from requests import post, Response
from logging import Logger, getLogger

from resources.config import *
from resources.styles import *
from resources.functions import *
from components.titles import MainTitle


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class PermissionsView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page
		self.gl: ft.Geolocator = ft.Geolocator(
			location_settings=ft.GeolocatorSettings(
				accuracy=ft.GeolocatorPositionAccuracy.LOW
			),
			on_error=lambda error: logger.error(f"Geolocator error: {error}"),
		)
		self.page.overlay.append(self.gl)

		# Custom components
		self.btn_yes: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			content=ft.Text(value="Otorgar permisos", size=BTN_TEXT_SIZE),
			on_click=self.btn_yes_clicked,
			**btn_primary_style
		)
		self.btn_no: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			content=ft.Text(value="Continuar sin ubicación", size=BTN_TEXT_SIZE),
			on_click=self.btn_no_clicked,
			**btn_secondary_style,
		)

		# View native attributes
		super().__init__(
			route="/permissions",
			bgcolor=MAIN_COLOR,
			padding=ft.padding.all(value=0.0),
			controls=[
				ft.Container(
					content=ft.Column(
						scroll=ft.ScrollMode.HIDDEN,
						controls=[
							ft.Container(
								content=ft.IconButton(
									icon=ft.icons.ARROW_BACK,
									icon_color=ft.colors.BLACK,
									on_click=lambda _: go_to_view(page=self.page, logger=logger, route="/sign_in"),
								)
							),
							MainTitle(
								subtitle="Permisos de ubicación",
								top_margin=(SPACING * 2),
							),
							ft.Container(
								margin=ft.margin.only(top=(SPACING * 3)),
								content=ft.Text(
									value=(
										"Para utilizar las funcionalidades de recomendación de sitios "
										"turísticos cercanos a tu posición actual, así como para disfrutar "
										"del mapa interactivo, es necesario otorgar los permisos de ubicación.\n\n"
										"Puedes continuar sin otorgarlos, pero dichas funcionalidades "
										"no estarán disponibles hasta que permitas el uso de tu ubicación."
									),
									color=ft.colors.BLACK
								)
							),
							ft.Container(
								margin=ft.margin.only(top=(SPACING * 3)),
								content=ft.Column(
									controls=[
										self.btn_yes,
										ft.Divider(color=ft.colors.TRANSPARENT),
										self.btn_no
									]
								)
							),
						]
					),
					**cont_main_style
				)
			]
		)

	def btn_yes_clicked(self, _: ft.ControlEvent) -> None:
		logger.info("Checking location permissions...")
		if request_location_permissions(self.gl, logger):
			logger.info("Location permissions granted. Getting current coordinates...")
			current_position: ft.GeolocatorPosition = self.gl.get_current_position()
			self.page.session.set(key="current_latitude", value=current_position.latitude)
			self.page.session.set(key="current_longitude", value=current_position.longitude)
			logger.info(f"Got current coordinates: ({current_position.latitude}, {current_position.longitude})")

			self.page.session.set(
				key="is_inside_cdmx",
				value=(
					True
					if is_inside_cdmx((
						self.page.session.get("current_latitude"),
						self.page.session.get("current_longitude")
					))
					else False
				)
			)
			self.page.session.set(
				key="chk_distance_value",
				value=(
					True
					if self.page.session.get("is_inside_cdmx")
					else False
				)
			)

		go_to_view(page=self.page, logger=logger, route='/')

	def btn_no_clicked(self, _: ft.ControlEvent) -> None:
		logger.warning("Location permissions are not granted. Continuing without coordinates...")
		self.page.session.set(key="current_latitude", value=None)
		self.page.session.set(key="current_longitude", value=None)

		self.page.session.set(key="is_inside_cdmx", value=False)
		self.page.session.set(key="chk_distance_value", value=False)

		go_to_view(page=self.page, logger=logger, route='/')
