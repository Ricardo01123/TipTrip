import flet as ft
from logging import Logger, getLogger

from resources.config import *
from resources.styles import *
from resources.functions import *
from components.titles import MainTitle
# from components.geolocator import geolocator


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class PermissionsView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page
		# self.gl: ft.Geolocator = geolocator
		self.gl: ft.Geolocator = ft.Geolocator(
			location_settings=ft.GeolocatorSettings(
				accuracy=ft.GeolocatorPositionAccuracy.LOW
			),
			on_error=lambda error: logger.error(f"Geolocator error: {error}"),
		)
		self.page.overlay.append(self.gl)

		# Custom components
		self.btn_submit: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			content=ft.Text(value="Continuar", size=BTN_TEXT_SIZE),
			on_click=self.btn_submit_clicked,
			**btn_primary_style
		)
		self.btn_logout: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			content=ft.Text(value="Salir", size=BTN_TEXT_SIZE),
			on_click=self.btn_logout_clicked,
			**btn_secondary_style,
		)

		self.dlg_location_permissions_denied: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text("Permisos de ubicación"),
			content=ft.Text(
				"No se han otorgado los permisos de ubicación. "
				"Para continuar, es necesario otorgar los permisos de ubicación."
			),
			actions_alignment=ft.MainAxisAlignment.END,
			actions=[
				ft.TextButton(
					text="Aceptar",
					on_click=lambda _: self.page.close(self.dlg_location_permissions_denied)
				)
			],
			on_dismiss=lambda _: self.page.close(self.dlg_location_permissions_denied)
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
										"Para poder brindarte una mejor experiencia, "
										"necesitamos acceder a tu ubicación. "
									),
									color=ft.colors.BLACK
								)
							),
							ft.Container(
								margin=ft.margin.only(top=(SPACING * 3)),
								content=ft.Column(
									controls=[
										self.btn_submit,
										ft.Divider(color=ft.colors.TRANSPARENT),
										self.btn_logout
									]
								)
							),
						]
					),
					**cont_main_style
				)
			]
		)

	def btn_submit_clicked(self, _: ft.ControlEvent) -> None:
		logger.info("Checking location permissions...")
		if request_location_permissions(self.gl, logger):
			logger.info("Location permissions granted. Getting current coordinates...")
			current_position: ft.GeolocatorPosition = self.gl.get_current_position()
			self.page.session.set(key="current_latitude", value=current_position.latitude)
			self.page.session.set(key="current_longitude", value=current_position.longitude)
			logger.info(f"Got current coordinates: ({current_position.latitude}, {current_position.longitude})")

			go_to_view(page=self.page, logger=logger, route='/')

		else:
			logger.warning("Location permissions are not granted")
			self.page.open(self.dlg_location_permissions_denied)

	def btn_logout_clicked(self, _: ft.ControlEvent) -> None:
		logger.info("Cleaning session...")
		self.page.session.clear()

		go_to_view(page=self.page, logger=logger, route="/sign_in")
