import flet as ft
from os import listdir
from os.path import join
from requests import get, Response
from logging import Logger, getLogger
from requests import post, delete, Response

from components.bars import *
from resources.config import *
from components.carousel import Carousel
from resources.functions import get_place_icon


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class PlaceDetailsView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page
		self.place_data: dict | ft.Container = self.get_place_data(self.page.session.get("place_id"))

		# Custom components
		self.saved_iconbutton: ft.IconButton = ft.IconButton(
			icon=(
				ft.Icons.BOOKMARKS
				if self.place_data["is_favorite"]
				else ft.Icons.BOOKMARKS_OUTLINED
			),
			icon_color=SECONDARY_COLOR,
			icon_size=25,
			on_click=self.handle_saved_iconbutton
		)
		self.data_tabs: ft.Tabs = ft.Tabs(
			selected_index=0,
			animation_duration=300,
			divider_color=ft.Colors.TRANSPARENT,
			indicator_color=ft.Colors.TRANSPARENT,
			label_color=MAIN_COLOR,
			unselected_label_color=ft.Colors.BLACK,
			tabs=self.fill_data_tabs()
		)

		# View native attributes
		super().__init__(
			route="/place_details",
			bgcolor=ft.Colors.WHITE,
			padding=ft.padding.all(value=0.0),
			spacing=0,
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
					),
				),
				ft.Container(
					width=self.page.width,
					alignment=ft.alignment.center,
					padding=ft.padding.only(
						top=(SPACING / 2),
						right=SPACING,
						bottom=10,
						left=SPACING
					),
					content=ft.Container(
						height=90,
						bgcolor=ft.Colors.WHITE,
						padding=ft.padding.symmetric(
							vertical=(SPACING / 2),
							horizontal=SPACING
						),
						border_radius=ft.border_radius.all(value=RADIUS),
						shadow=ft.BoxShadow(
							blur_radius=LOW_BLUR,
							color=ft.Colors.GREY_500
						),
						content=(
							self.place_data
							if isinstance(self.place_data, ft.Container)
							else ft.Column(
								alignment=ft.MainAxisAlignment.CENTER,
								spacing=0,
								controls=[
									ft.Container(
										width=self.page.width,
										alignment=ft.alignment.bottom_left,
										content=ft.Row(
											scroll=ft.ScrollMode.HIDDEN,
											controls=[
												ft.Text(
													value=self.place_data["info"]["name"],
													color=MAIN_COLOR,
													weight=ft.FontWeight.BOLD,
													size=25,
												)
											]
										)
									),
									ft.Container(
										width=self.page.width,
										content=ft.Row(
											spacing=0,
											alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
											controls=[
												ft.Container(
													content=ft.Row(
														spacing=10,
														controls=[
															ft.Container(content=self.saved_iconbutton),
															ft.Container(
																content=ft.Icon(
																	name=get_place_icon(self.place_data["info"]["classification"]),
																	color=SECONDARY_COLOR,
																	size=18
																)
															),
															ft.Container(
																content=ft.Text(
																	value=self.place_data["info"]["classification"],
																	color=SECONDARY_COLOR,
																	size=18
																)
															)
														]
													)
												),
												ft.Container(
													width=70,
													bgcolor=SECONDARY_COLOR,
													border_radius=ft.border_radius.all(
														value=15
													),
													padding=ft.padding.only(
														right=5
													),
													content=ft.Row(
														spacing=5,
														alignment=ft.MainAxisAlignment.CENTER,
														controls=[
															ft.Container(
																expand=1,
																alignment=ft.alignment.center_right,
																content=ft.Icon(
																	name=ft.Icons.STAR_BORDER,
																	color=ft.Colors.WHITE,
																	size=18
																)
															),
															ft.Container(
																expand=1,
																alignment=ft.alignment.center_left,
																content=ft.Text(
																	value=self.place_data["info"]["punctuation"],
																	color=ft.Colors.WHITE,
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
				ft.Container(
					width=self.page.width,
					padding=ft.padding.only(
						right=10,
						left=10,
						bottom=10,
					),
					alignment=ft.alignment.center,
					content=Carousel(
						page=self.page,
						items=self.place_data["images"]
					)
				),
				ft.Container(
					expand=True,
					bgcolor=ft.Colors.WHITE,
					padding=ft.padding.symmetric(
						vertical=(SPACING / 2),
						horizontal=SPACING,
					),
					border_radius=ft.border_radius.only(
						top_left=RADIUS,
						top_right=RADIUS
					),
					shadow=ft.BoxShadow(
						blur_radius=LOW_BLUR,
						offset=ft.Offset(0, -2),
						color=ft.Colors.BLACK
					),
					content=ft.Column(
						expand=True,
						scroll=ft.ScrollMode.HIDDEN,
						controls=[self.data_tabs]
					)
				)
			],
			bottom_appbar=BottomBar(page=self.page, logger=logger, current_route="/place_details")
		)

	def get_place_data(self, id: str) -> dict | ft.Container:
		response: Response = get(
			url=f"{BACK_END_URL}/{PLACES_ENDPOINT}/{id}",
			headers={
				"Content-Type": "application/json",
				"Authorization": f"Bearer {self.page.session.get('session_token')}"
			},
			json={
				"current_latitude": self.page.session.get("current_latitude"),
				"current_longitude": self.page.session.get("current_longitude")
			}
		)

		if response.status_code == 200:
			logger.debug(f"Response 200 OK: {response.json()}")
			return response.json()["place"]

		elif response.status_code == 204:
			logger.debug(f"Response 204 No Content: {response.json()}")
			return ft.Container(
				alignment=ft.alignment.center,
				content=ft.Text(
					value="No se encontró información del sitio turístico seleccionado.",
					color=ft.Colors.BLACK,
					size=30
				)
			)

		else:
			logger.error(f"Response {response.status_code}: {response.json()}")
			return ft.Container(
				alignment=ft.alignment.center,
				content=ft.Text(
					value=(
						"Ocurrió un error al obtener información del sitio "
						"turístico seleccionado.\n"
						"Favor de intentarlo de nuevo más tarde."
					),
					color=ft.Colors.BLACK,
					size=35
				)
			)

	def fill_data_tabs(self) -> list:
		result: list = []

		if any([
			self.place_data["distance"],
			self.place_data["info"]["schedules"],
			self.place_data["info"]["prices"],
			self.place_data["address"]["street_number"],
			self.place_data["address"]["colony"],
			self.place_data["address"]["cp"],
			self.place_data["address"]["municipality"],
			self.place_data["address"]["state"],
			self.place_data["address"]["how_to_arrive"],
		]):
			info: ft.Column = ft.Column()

			if self.place_data["distance"]:
				info.controls.append(
					ft.Container(
						content=ft.Column(
							controls=[
								ft.Container(
									content=ft.Text(
										value=f"Distancia de mí:",
										weight=ft.FontWeight.BOLD,
										color=ft.Colors.BLACK
									)
								),
								ft.Container(
									content=ft.Text(
										value=f"{self.place_data['distance']:.2f} km",
										color=ft.Colors.BLACK
									)
								)
							]
						)
					)
				)
			if self.place_data["info"]["schedules"]:
				info.controls.append(
					ft.Container(
						content=ft.Column(
							controls=[
								ft.Container(
									content=ft.Text(
										value=f"\nHorarios:",
										weight=ft.FontWeight.BOLD,
										color=ft.Colors.BLACK
									)
								),
								ft.Container(
									content=ft.Text(
										value=self.place_data["info"]["schedules"],
										color=ft.Colors.BLACK,
										text_align=ft.TextAlign.JUSTIFY
									)
								)
							]
						)
					)
				)

			if self.place_data["info"]["prices"]:
				info.controls.append(
					ft.Container(
						content=ft.Column(
							controls=[
								ft.Container(
									content=ft.Text(
										value=f"\nCostos:",
										weight=ft.FontWeight.BOLD,
										color=ft.Colors.BLACK
									)
								),
								ft.Container(
									content=ft.Text(
										value=self.place_data["info"]["prices"],
										color=ft.Colors.BLACK,
										text_align=ft.TextAlign.JUSTIFY
									)
								)
							]
						)
					)
				)

			if any([
				self.place_data["address"]["street_number"],
				self.place_data["address"]["colony"],
				self.place_data["address"]["cp"],
				self.place_data["address"]["municipality"],
				self.place_data["address"]["state"],
			]):
				info.controls.append(
					ft.Container(
						content=ft.Column(
							controls=[
								ft.Container(
									content=ft.Text(
										value=f"\nDirección:",
										weight=ft.FontWeight.BOLD,
										color=ft.Colors.BLACK
									)
								),
								ft.Container(
									content=ft.Text(
										value=(
											f"{self.place_data['address']['street_number']}, "
											f"{self.place_data['address']['colony']}, "
											f"{self.place_data['address']['cp']}, "
											f"{self.place_data['address']['municipality']}, "
											f"{self.place_data['address']['state']}."
										),
										color=ft.Colors.BLACK,
										text_align=ft.TextAlign.JUSTIFY
									)
								)
							]
						)
					)
				)

			if self.place_data["address"]["how_to_arrive"]:
				info.controls.append(
					ft.Container(
						content=ft.Column(
							controls=[
								ft.Container(
									content=ft.Text(
										value=f"\nReferencias para llegar:",
										weight=ft.FontWeight.BOLD,
										color=ft.Colors.BLACK
									)
								),
								ft.Container(
									content=ft.Text(
										value=self.place_data["address"]["how_to_arrive"],
										color=ft.Colors.BLACK,
										text_align=ft.TextAlign.JUSTIFY
									)
								)
							]
						)
					)
				)

			result.append(
				ft.Tab(
					text="Información",
					content=info
				)
			)

		if self.place_data["info"]["description"]:
			result.append(
				ft.Tab(
					text="Descripción",
					content=ft.Container(
						content=ft.Text(
							value=self.place_data["info"]["description"],
							color=ft.Colors.BLACK,
							text_align=ft.TextAlign.JUSTIFY
						)
					)
				)
			)

		if self.place_data["reviews"]["historic"]:
			result.append(
				ft.Tab(
					text="Reseña histórica",
					content=ft.Container(
						content=ft.Text(
							value=self.place_data["reviews"]["historic"],
							color=ft.Colors.BLACK,
							text_align=ft.TextAlign.JUSTIFY
						)
					)
				)
			)

		if self.place_data["reviews"]["general"]:
			result.append(
				ft.Tab(
					text="Reseña general",
					content=ft.Container(
						content=ft.Text(
							value=self.place_data["reviews"]["general"],
							color=ft.Colors.BLACK,
							text_align=ft.TextAlign.JUSTIFY
						)
					)
				)
			)

		if self.place_data["info"]["services"]:
			result.append(
				ft.Tab(
					text="Servicios",
					content=ft.Container(
						content=ft.Text(
							value=self.place_data["info"]["services"],
							color=ft.Colors.BLACK,
							text_align=ft.TextAlign.JUSTIFY
						)
					)
				)
			)

		if self.place_data["info"]["activities"]:
			result.append(
				ft.Tab(
					text="Actividades",
					content=ft.Container(
						content=ft.Text(
							value=self.place_data["info"]["activities"],
							color=ft.Colors.BLACK,
							text_align=ft.TextAlign.JUSTIFY
						)
					)
				)
			)

		if self.place_data["info"]["permanent_exhibitions"]:
			result.append(
				ft.Tab(
					text="Salas permanentes",
					content=ft.Container(
						content=ft.Text(
							value=self.place_data["info"]["permanent_exhibitions"],
							color=ft.Colors.BLACK,
							text_align=ft.TextAlign.JUSTIFY
						)
					)
				)
			)

		if self.place_data["info"]["temporal_exhibitions"]:
			result.append(
				ft.Tab(
					text="Salas temporales",
					content=ft.Container(
						content=ft.Text(
							value=self.place_data["info"]["temporal_exhibitions"],
							color=ft.Colors.BLACK,
							text_align=ft.TextAlign.JUSTIFY
						)
					)
				)
			)

		if any([
			self.place_data["info"]["mail"],
			self.place_data["info"]["phone"],
			self.place_data["info"]["website"],
			self.place_data["info"]["sic_website"]
		]):
			contact_info: ft.Column = ft.Column()

			if self.place_data["info"]["mail"]:
				contact_info.controls.append(
					ft.Container(
						content=ft.Column(
							controls=[
								ft.Container(
									content=ft.Text(
										value=f"\nCorreo electrónico:",
										weight=ft.FontWeight.BOLD,
										color=ft.Colors.BLACK
									)
								),
								ft.Container(
									content=ft.Text(
										value=self.place_data["info"]["mail"],
										color=ft.Colors.BLACK,
										text_align=ft.TextAlign.JUSTIFY
									)
								)
							]
						)
					)
				)

			if self.place_data["info"]["phone"]:
				contact_info.controls.append(
					ft.Container(
						content=ft.Column(
							controls=[
								ft.Container(
									content=ft.Text(
										value=f"\nTeléfono:",
										weight=ft.FontWeight.BOLD,
										color=ft.Colors.BLACK
									)
								),
								ft.Container(
									content=ft.Text(
										value=self.place_data["info"]["phone"],
										color=ft.Colors.BLACK
									)
								)
							]
						)
					)
				)

			if self.place_data["info"]["website"]:
				contact_info.controls.append(
					ft.Container(
						content=ft.Column(
							controls=[
								ft.Container(
									content=ft.Text(
										value=f"\nPágina web:",
										weight=ft.FontWeight.BOLD,
										color=ft.Colors.BLACK
									)
								),
								ft.Container(
									content=ft.Text(
										value=self.place_data["info"]["website"],
										color=ft.Colors.BLACK,
										text_align=ft.TextAlign.JUSTIFY
									)
								)
							]
						)
					)
				)

			if self.place_data["info"]["sic_website"]:
				contact_info.controls.append(
					ft.Container(
						content=ft.Column(
							controls=[
								ft.Container(
									content=ft.Text(
										value=f"\nPágina del gobierno (SIC):",
										weight=ft.FontWeight.BOLD,
										color=ft.Colors.BLACK
									)
								),
								ft.Container(
									content=ft.Text(
										value=self.place_data["info"]["sic_website"],
										color=ft.Colors.BLACK,
										text_align=ft.TextAlign.JUSTIFY
									)
								)
							]
						)
					)
				)

			result.append(
				ft.Tab(
					text="Contacto",
					content=contact_info
				)
			)

		if result == []:
			result.append(
				ft.Tab(
					text="Error",
					content=ft.Container(
						content=ft.Text(
							value="No se encontró información",
							color=ft.Colors.BLACK
						)
					)
				)
			)

		return result

	def handle_saved_iconbutton(self, _) -> None:
		if self.saved_iconbutton.icon == ft.Icons.BOOKMARKS:
			logger.info("Removing place from favorites...")
			response: Response = delete(
				url=f"{BACK_END_URL}/{FAVORITES_ENDPOINT}/{self.page.session.get('id')}/{self.place_data['id']}",
				headers={
					"Content-Type": "application/json",
					"Authorization": f"Bearer {self.page.session.get('session_token')}"
				}
			)

			if response.status_code == 200:
				logger.info("Place removed from favorites successfully")
				self.saved_iconbutton.icon = ft.Icons.BOOKMARKS_OUTLINED
				self.page.update()
			else:
				print("Error removing place from favorites")
				self.dlg_error.title = ft.Text("Error al eliminar")
				self.dlg_error.content = ft.Text(
					"Ocurrió un error eliminando el sitio turístico de la lista de favoritos. "
					"Favor de intentarlo de nuevo más tarde."
				)
				self.page.open(self.dlg_error)

		else:
			logger.info("Adding place to favorites...")
			response: Response = post(
				url=f"{BACK_END_URL}/{FAVORITES_ENDPOINT}",
				headers={
					"Content-Type": "application/json",
					"Authorization": f"Bearer {self.page.session.get('session_token')}"
				},
				json={
					"user_id": self.page.session.get("id"),
					"place_id": self.place_data["id"]
				}
			)

			if response.status_code == 201:
				logger.info("Place added to favorites successfully")
				self.saved_iconbutton.icon = ft.Icons.BOOKMARKS
				self.page.update()
			else:
				print("Error adding place to favorites")
				self.dlg_error.title = ft.Text("Error al agregar")
				self.dlg_error.content = ft.Text(
					"Ocurrió un error agregando el sitio turístico a la lista de favoritos. "
					"Favor de intentarlo de nuevo más tarde."
				)
				self.page.open(self.dlg_error)
