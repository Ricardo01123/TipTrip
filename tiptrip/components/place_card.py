import flet as ft
from logging import Logger, getLogger

from requests import post, delete, Response
from requests.exceptions import ConnectTimeout

from resources.config import *
from resources.functions import go_to_view, get_place_icon


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class PlaceCard(ft.Container):
	def __init__(
			self,
			page: ft.Page,
			id: int,
			name: str,
			classification: str,
			address: str,
			image_name: str,
			is_favorite: bool,
			punctuation: int = None,
			distance: float = None,
		) -> None:

		self.page: ft.Page = page
		self.place_id: int = id

		super().__init__(
			bgcolor=ft.Colors.WHITE,
			padding=ft.padding.only(
				left=(SPACING / 2),
				top=(SPACING / 2),
				right=(SPACING / 2),
				bottom=0,
			),
			border_radius=ft.border_radius.all(RADIUS),
			shadow=ft.BoxShadow(
				blur_radius=LOW_BLUR,
				offset=ft.Offset(0, 3),
				color=ft.Colors.GREY
			),
			on_click=self.open_place_details_view
		)

		self.saved_iconbutton: ft.IconButton = ft.IconButton(
			icon=(
				ft.Icons.BOOKMARKS
				if is_favorite
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
				ft.TextButton("Aceptar", on_click=lambda _: self.page.close(self.dlg_error)),
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_error)
		)

		self.content=ft.Column(
			controls=[
				ft.Container(
					content=ft.Row(
						scroll=ft.ScrollMode.HIDDEN,
						controls=[
							ft.Text(
								value=name,
								color=MAIN_COLOR,
								size=PLC_TITLE_SIZE,
								weight=ft.FontWeight.BOLD,
								selectable=True
							)
						]
					)
				),
				ft.Container(
					content=ft.Row(
						controls=[
							ft.Container(
								expand=1,
								content=ft.Image(
									src=image_name,
									fit=ft.ImageFit.FILL,
									repeat=ft.ImageRepeat.NO_REPEAT,
									border_radius=ft.border_radius.all(RADIUS)
								)
							),
							ft.Container(
								expand=1,
								content=ft.Column(
									controls=[
										ft.Container(
											content=ft.Row(
												spacing=3,
												alignment=ft.MainAxisAlignment.START,
												controls=[
													ft.Container(
														content=ft.Icon(
															name=get_place_icon(classification),
															color=SECONDARY_COLOR,
															size=20
														)
													),
													ft.Container(
														content=ft.Text(
															value=classification,
															color=SECONDARY_COLOR,
															size=PLC_CATEGORY_SIZE,
															selectable=True
														)
													)
												]
											)
										),
										ft.Container(
											content=ft.Text(
												value=address,
												color=ft.Colors.BLACK,
												selectable=True
											)
										)
									]
								)
							)
						]
					)
				),
				ft.Container(
					content=ft.Row(
						alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
						spacing=0,
						controls=[
							ft.Container(content=self.saved_iconbutton),
							ft.Container(
								content=ft.Text(
									value=(
										f"Distancia de mí: {distance:.2f} km"
										if distance is not None
										else ""
									),
									color=(
										ft.Colors.BLACK
										if distance is not None
										else ft.Colors.WHITE
									),
									selectable=(
										True
										if distance is not None
										else False
									)
								)
							),
							ft.Container(
								width=60,
								bgcolor=(
									SECONDARY_COLOR
									if punctuation is not None
									else ft.Colors.RED
								),
								border_radius=ft.border_radius.all(
									value=15
								),
								padding=ft.padding.only(
									right=5
								),
								content=ft.Row(
									spacing=0,
									alignment=ft.MainAxisAlignment.CENTER,
									controls=(
										[
											ft.Container(
												expand=1,
												alignment=ft.alignment.center_right,
												content=ft.Icon(
													name=ft.Icons.STAR_BORDER,
													color=ft.Colors.WHITE,
													size=14
												)
											),
											ft.Container(
												expand=1,
												alignment=ft.alignment.center_left,
												content=ft.Text(
													value=punctuation,
													color=ft.Colors.WHITE,
												)
											)
										]
										if punctuation is not None else
										[
											ft.Container(
												expand=True,
												margin=ft.margin.symmetric(
													vertical=3
												),
												alignment=ft.alignment.center,
												content=ft.Icon(
													name=ft.Icons.STAR_BORDER,
													color=ft.Colors.WHITE,
													size=14
												)
											)
										]
									)
								)
							)
						]
					)
				)
			]
		)

	def open_place_details_view(self, _: ft.ControlEvent) -> None:
		self.page.session.set(key="place_id", value=self.place_id)
		try:
			go_to_view(page=self.page, logger=logger, route="/place_details")
		except Exception as e:
			logger.error(f"Error: {e}")
			go_to_view(page=self.page, logger=logger, route="/place_details")

	def handle_saved_iconbutton(self, _: ft.ControlEvent) -> None:
		if self.saved_iconbutton.icon == ft.Icons.BOOKMARKS:
			logger.info("Removing place from favorites...")
			try:
				response: Response = delete(
					url=f"{BACK_END_URL}/{FAVORITES_ENDPOINT}/{self.page.session.get('id')}/{self.place_id}",
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
						"place_id": self.place_id
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
					return

			if response.status_code == 201:
				logger.info("Place added to favorites successfully")
				self.saved_iconbutton.icon = ft.Icons.BOOKMARKS
				try:
					self.page.update()
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.update()
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
