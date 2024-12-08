import flet as ft
from os import listdir
from os.path import join
from logging import Logger, getLogger

from requests.exceptions import ConnectTimeout
from requests import get, post, delete, Response

from components.bars import *
from resources.config import *
from resources.functions import *
from components.carousel import Carousel


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
				if not isinstance(self.place_data, ft.Container) and self.place_data["is_favorite"]
				else ft.Icons.BOOKMARKS_OUTLINED
			),
			icon_color=SECONDARY_COLOR,
			icon_size=25,
			on_click=self.handle_saved_iconbutton
		)
		self.dlg_error: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text(""),
			content=ft.Text(""),
			actions=[
				ft.TextButton(
					text="Aceptar",
					on_click=lambda _: self.page.close(self.dlg_error)
				),
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_error)
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
						content=ft.Column(
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
												selectable=True
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
																size=18,
																selectable=True
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
																size=18,
																selectable=True
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
						items=self.get_items()
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
					content=ft.Tabs(
						selected_index=0,
						animation_duration=300,
						divider_color=ft.Colors.TRANSPARENT,
						indicator_color=ft.Colors.TRANSPARENT,
						label_color=MAIN_COLOR,
						unselected_label_color=ft.Colors.BLACK,
						tabs=self.fill_data_tabs()
					)
				)
			],
			bottom_appbar=BottomBar(page=self.page, logger=logger, current_route="/place_details")
		)

	def get_place_data(self, id: str) -> dict | ft.Container:
		try:
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
		except ConnectTimeout:
			logger.error("Connection timeout while deleting account")
			self.dlg_error.title = ft.Text(value="Error de conexión a internet")
			self.dlg_error.content = ft.Text(
				value=(
					"No se pudo obtener información del sitio turístico seleccionado. "
					"Favor de revisar su conexión a internet e intentarlo de nuevo más tarde."
				)
			)

			try:
				self.page.open(self.dlg_error)

			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.open(self.dlg_error)

			finally:
				ft.Container(
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

		if response.status_code == 200:
			logger.debug(f"Response 200 OK: {response.json()}")
			return response.json()["place"]

		elif response.status_code == 204 or response.status_code == 404:
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
			#! COMMENT
			post(
				url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
				headers={"Content-Type": "application/json"},
				json={
					"user_id": self.page.session.get("id"),
					"file": encode_logfile()
				}
			)
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
			info: ft.Column = ft.Column(scroll=ft.ScrollMode.HIDDEN)

			if self.place_data["distance"]:
				info.controls.append(
					ft.Container(
						content=ft.Column(
							controls=[
								ft.Container(
									content=ft.Text(
										value=f"Distancia de mí:",
										weight=ft.FontWeight.BOLD,
										color=ft.Colors.BLACK,
										selectable=True
									)
								),
								ft.Container(
									content=ft.Text(
										value=f"{self.place_data['distance']:.2f} km",
										color=ft.Colors.BLACK,
										selectable=True
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
										color=ft.Colors.BLACK,
										selectable=True
									)
								),
								ft.Container(
									content=ft.Text(
										value=self.place_data["info"]["schedules"],
										color=ft.Colors.BLACK,
										text_align=ft.TextAlign.JUSTIFY,
										selectable=True
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
										color=ft.Colors.BLACK,
										selectable=True
									)
								),
								ft.Container(
									content=ft.Text(
										value=self.place_data["info"]["prices"],
										color=ft.Colors.BLACK,
										text_align=ft.TextAlign.JUSTIFY,
										selectable=True
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
										color=ft.Colors.BLACK,
										selectable=True
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
										text_align=ft.TextAlign.JUSTIFY,
										selectable=True
									)
								)
							]
						)
					)
				)

			if self.place_data["address"]["how_to_arrive"]:
				splitted: list = split_text(self.place_data["address"]["how_to_arrive"])
				info.controls.append(
					ft.Container(
						content=ft.Column(
							controls=[
								ft.Container(
									content=ft.Text(
										value=f"\nReferencias para llegar:",
										weight=ft.FontWeight.BOLD,
										color=ft.Colors.BLACK,
										selectable=True
									)
								),
								ft.Container(
									content=ft.Column(
										scroll=ft.ScrollMode.HIDDEN,
										controls=[
											ft.Text(
												value=split,
												color=ft.Colors.BLACK,
												text_align=ft.TextAlign.JUSTIFY,
												selectable=True
											) for split in splitted
										]
									)
								)
							]
						)
					)
				)

			result.append(
				ft.Tab(
					text="Información",
					content=ft.Container(
						expand=True,
						content=info
					)
				)
			)

		if self.place_data["info"]["description"]:
			splitted: list = split_text(self.place_data["info"]["description"])
			result.append(
				ft.Tab(
					text="Descripción",
					content=ft.Container(
						expand=True,
						content=ft.Column(
							scroll=ft.ScrollMode.HIDDEN,
							controls=[
								ft.Text(
									value=split,
									color=ft.Colors.BLACK,
									text_align=ft.TextAlign.JUSTIFY,
									selectable=True
								) for split in splitted
							]
						)
					)
				)
			)

		if self.place_data["reviews"]["historic"]:
			splitted: list = split_text(self.place_data["reviews"]["historic"])
			result.append(
				ft.Tab(
					text="Reseña histórica",
					content=ft.Container(
						expand=True,
						content=ft.Column(
							scroll=ft.ScrollMode.HIDDEN,
							controls=[
								ft.Text(
									value=split,
									color=ft.Colors.BLACK,
									text_align=ft.TextAlign.JUSTIFY,
									selectable=True
								) for split in splitted
							]
						)
					)
				)
			)

		if self.place_data["reviews"]["general"]:
			splitted: list = split_text(self.place_data["reviews"]["general"])
			result.append(
				ft.Tab(
					text="Reseña general",
					content=ft.Container(
						expand=True,
						content=ft.Column(
							scroll=ft.ScrollMode.HIDDEN,
							controls=[
								ft.Text(
									value=split,
									color=ft.Colors.BLACK,
									text_align=ft.TextAlign.JUSTIFY,
									selectable=True
								) for split in splitted
							]
						)
					)
				)
			)

		if self.place_data["info"]["services"]:
			splitted: list = split_text(self.place_data["info"]["services"])
			result.append(
				ft.Tab(
					text="Servicios",
					content=ft.Container(
						expand=True,
						content=ft.Column(
							scroll=ft.ScrollMode.HIDDEN,
							controls=[
								ft.Text(
									value=split,
									color=ft.Colors.BLACK,
									text_align=ft.TextAlign.JUSTIFY,
									selectable=True
								) for split in splitted
							]
						)
					)
				)
			)

		if self.place_data["info"]["activities"]:
			splitted: list = split_text(self.place_data["info"]["activities"])
			result.append(
				ft.Tab(
					text="Actividades",
					content=ft.Container(
						expand=True,
						content=ft.Column(
							scroll=ft.ScrollMode.HIDDEN,
							controls=[
								ft.Text(
									value=split,
									color=ft.Colors.BLACK,
									text_align=ft.TextAlign.JUSTIFY,
									selectable=True
								) for split in splitted
							]
						)
					)
				)
			)

		if self.place_data["info"]["permanent_exhibitions"]:
			splitted: list = split_text(self.place_data["info"]["permanent_exhibitions"])
			result.append(
				ft.Tab(
					text="Salas permanentes",
					content=ft.Container(
						expand=True,
						content=ft.Column(
							scroll=ft.ScrollMode.HIDDEN,
							controls=[
								ft.Text(
									value=split,
									color=ft.Colors.BLACK,
									text_align=ft.TextAlign.JUSTIFY,
									selectable=True
								) for split in splitted
							]
						)
					)
				)
			)

		if self.place_data["info"]["temporal_exhibitions"]:
			splitted: list = split_text(self.place_data["info"]["temporal_exhibitions"])
			result.append(
				ft.Tab(
					text="Salas temporales",
					content=ft.Container(
						expand=True,
						content=ft.Column(
							scroll=ft.ScrollMode.HIDDEN,
							controls=[
								ft.Text(
									value=split,
									color=ft.Colors.BLACK,
									text_align=ft.TextAlign.JUSTIFY,
									selectable=True
								) for split in splitted
							]
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
			contact_info: ft.Column = ft.Column(scroll=ft.ScrollMode.HIDDEN)

			if self.place_data["info"]["mail"]:
				contact_info.controls.append(
					ft.Container(
						content=ft.Column(
							controls=[
								ft.Container(
									content=ft.Text(
										value="Correo electrónico:",
										weight=ft.FontWeight.BOLD,
										color=ft.Colors.BLACK,
										selectable=True
									)
								),
								ft.Container(
									content=ft.Text(
										value=self.place_data["info"]["mail"],
										color=ft.Colors.BLACK,
										text_align=ft.TextAlign.JUSTIFY,
										selectable=True
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
										color=ft.Colors.BLACK,
										selectable=True
									)
								),
								ft.Container(
									content=ft.Text(
										value=self.place_data["info"]["phone"],
										color=ft.Colors.BLACK,
										text_align=ft.TextAlign.JUSTIFY,
										selectable=True
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
										color=ft.Colors.BLACK,
										selectable=True
									)
								),
								ft.Container(
									content=ft.Markdown(
										value=(
											f"[{self.place_data['info']['website']}]"
											f"({self.place_data['info']['website']})"
										),
										md_style_sheet=ft.MarkdownStyleSheet(
											p_text_style=ft.TextStyle(color=ft.Colors.BLACK)
										),
										on_tap_link=lambda e: self.page.launch_url(e.data)
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
										color=ft.Colors.BLACK,
										selectable=True
									)
								),
								ft.Container(
									content=ft.Markdown(
										value=(
											f"[{self.place_data['info']['sic_website']}]"
											f"({self.place_data['info']['sic_website']})"
										),
										md_style_sheet=ft.MarkdownStyleSheet(
											p_text_style=ft.TextStyle(color=ft.Colors.BLACK)
										),
										on_tap_link=lambda e: self.page.launch_url(e.data)
									)
								)
							]
						)
					)
				)

			result.append(
				ft.Tab(
					text="Contacto",
					content=ft.Container(
						expand=True,
						content=contact_info
					)
				)
			)

		if result == []:
			result.append(
				ft.Tab(
					text="Error",
					content=ft.Container(
						expand=True,
						content=ft.Text(
							value="No se encontró información sobre el sitio turístico seleccionado.",
							color=ft.Colors.BLACK,
							text_align=ft.TextAlign.JUSTIFY
						)
					)
				)
			)

		return result

	def get_items(self) -> list:
		image_dir: str = format_place_name(self.place_data["info"]["name"])
		path: str = join(ASSETS_ABSPATH, "places", image_dir)
		try:
			images: list = listdir(path)
			if images:
				return [join("places", image_dir, image) for image in images]
			else:
				return ["default.png"]

		except Exception:
			#! COMMENT
			post(
				url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
				headers={"Content-Type": "application/json"},
				json={
					"user_id": self.page.session.get("id"),
					"file": encode_logfile()
				}
			)
			return ["default.png"]

	def handle_saved_iconbutton(self, _) -> None:
		if self.saved_iconbutton.icon == ft.Icons.BOOKMARKS:
			logger.info("Removing place from favorites...")
			try:
				response: Response = delete(
					url=f"{BACK_END_URL}/{FAVORITES_ENDPOINT}/{self.page.session.get('id')}/{self.place_data['id']}",
					headers={
						"Content-Type": "application/json",
						"Authorization": f"Bearer {self.page.session.get('session_token')}"
					}
				)

			except ConnectTimeout:
				logger.error("Connection timeout while deleting favorite place")
				self.dlg_error.title = ft.Text("Error de conexión a internet")
				self.dlg_error.content = ft.Text(
					"No se pudo eliminar el sitio turístico de la lista de favoritos. "
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
					return

			if response.status_code == 200:
				logger.info("Place removed from favorites successfully")
				self.saved_iconbutton.icon = ft.Icons.BOOKMARKS_OUTLINED
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
				print("Error removing place from favorites")
				self.dlg_error.title = ft.Text("Error al eliminar")
				self.dlg_error.content = ft.Text(
					"Ocurrió un error eliminando el sitio turístico de la lista de favoritos. "
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

		else:
			logger.info("Adding place to favorites...")
			try:
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
			except ConnectTimeout:
				logger.error("Connection timeout while adding favorite place")
				self.dlg_error.title = ft.Text("Error de conexión a internet")
				self.dlg_error.content = ft.Text(
					"No se pudo agregar el sitio turístico a la lista de favoritos. "
					"Favor de revisar su conexión a internet e intentarlo de nuevo más tarde."
				)

				try:
					self.page.open(self.dlg_error)
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.open(self.dlg_error)

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
					return

			if response.status_code == 201:
				logger.info("Place added to favorites successfully")
				self.saved_iconbutton.icon = ft.Icons.BOOKMARKS
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
				logger.error("Error adding place to favorites")
				self.dlg_error.title = ft.Text("Error al agregar")
				self.dlg_error.content = ft.Text(
					"Ocurrió un error agregando el sitio turístico a la lista de favoritos. "
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
