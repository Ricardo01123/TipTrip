from flet import *
from logging import getLogger
from flet_route import Basket
from requests import post, delete, Response

from resources.config import *
from resources.functions import go_to_view


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class PlaceCard(Container):
	def __init__(
			self,
			page: Page,
			basket: Basket,
			id: int,
			name: str,
			classification: str,
			address: str,
			image_link: str,
			is_favorite: bool,
			punctuation: int = None,
			distance: float = None,
		) -> None:

		super().__init__(
			bgcolor=colors.WHITE,
			padding = padding.only(
				left=(SPACING / 2),
				top=(SPACING / 2),
				right=(SPACING / 2),
				bottom=0,
			),
			border_radius = border_radius.all(RADIUS),
			shadow = BoxShadow(
				blur_radius=LOW_BLUR,
				offset=Offset(0, 3),
				color=colors.GREY
			),
			on_click = lambda _: go_to_view(
				page=page,
				logger=logger,
				route=f"place_details/{id}"
			)
		)

		self.page: Page = page
		self.basket: Basket = basket
		self.place_id: int = id

		self.saved_iconbutton: IconButton = IconButton(
			icon=(
				icons.BOOKMARK
				if is_favorite
				else icons.BOOKMARK_BORDER
			),
			icon_color=SECONDARY_COLOR,
			icon_size=25,
			on_click=self.handle_saved_iconbutton
		)

		self.dlg_error: AlertDialog = AlertDialog(
			modal=True,
			title=Text(""),
			content=Text(""),
			actions=[
				TextButton("Aceptar", on_click=lambda _: self.page.close(self.dlg_error)),
			],
			actions_alignment=MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_error)
		)

		self.content=Column(
			controls=[
				Container(
					content=Row(
						scroll=ScrollMode.HIDDEN,
						controls=[
							Text(
								value=name,
								color=MAIN_COLOR,
								size=PLC_TITLE_SIZE,
								weight=FontWeight.BOLD,
							)
						]
					)
				),
				Container(
					content=Row(
						controls=[
							Container(
								expand=1,
								content=Image(
									src=image_link,
									fit=ImageFit.FILL,
									repeat=ImageRepeat.NO_REPEAT,
									border_radius=border_radius.all(RADIUS)
								)
							),
							Container(
								expand=1,
								content=Column(
									controls=[
										Container(
											content=Row(
												spacing=3,
												alignment=MainAxisAlignment.START,
												controls=[
													Container(
														content=Icon(
															name=icons.MUSEUM_SHARP,
															color=SECONDARY_COLOR,
															size=15
														)
													),
													Container(
														content=Text(
															value=classification,
															color=SECONDARY_COLOR,
															size=PLC_CATEGORY_SIZE
														)
													)
												]
											)
										),
										Container(
											content=Text(
												value=address,
												color=colors.BLACK
											)
										)
									]
								)
							),
						]
					),
				),
				Container(
					content=Row(
						alignment=MainAxisAlignment.SPACE_BETWEEN,
						spacing=0,
						controls=[
							Container(content=self.saved_iconbutton),
							Container(
								content=Text(
									value=(
										f"Distancia de mí: {distance:.2f} km"
										if distance is not None
										else "Distancia de mí: No disponible"
									),
									color=(
										colors.BLACK
										if distance is not None
										else colors.RED
									)
								)
							),
							Container(
								width=60,
								bgcolor=(
									SECONDARY_COLOR
									if punctuation is not None
									else colors.RED
								),
								border_radius=border_radius.all(
									value=15
								),
								padding=padding.only(
									right=5
								),
								content=Row(
									spacing=0,
									alignment=MainAxisAlignment.CENTER,
									controls=(
										[
											Container(
												expand=1,
												alignment=alignment.center_right,
												content=Icon(
													name=icons.STAR_BORDER,
													color=colors.WHITE,
													size=14
												)
											),
											Container(
												expand=1,
												alignment=alignment.center_left,
												content=Text(
													value=punctuation,
													color=colors.WHITE,
												)
											)
										]
										if punctuation is not None else
										[
											Container(
												expand=True,
												margin=margin.symmetric(
													vertical=3
												),
												alignment=alignment.center,
												content=Icon(
													name=icons.STAR_BORDER,
													color=colors.WHITE,
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

	def handle_saved_iconbutton(self, _) -> None:
		if self.saved_iconbutton.icon == icons.BOOKMARK:
			logger.info("Removing place from favorites...")
			response: Response = delete(
				url=f"{BACK_END_URL}/{FAVORITES_ENDPOINT}/{self.basket.get('id')}/{self.place_id}",
				headers={
					"Content-Type": "application/json",
					"Authorization": f"Bearer {self.basket.get('session_token')}"
				}
			)

			if response.status_code == 200:
				logger.info("Place removed from favorites successfully")
				self.saved_iconbutton.icon = icons.BOOKMARK_BORDER
				self.page.update()
			else:
				print("Error removing place from favorites")
				self.dlg_error.title = Text("Error al eliminar")
				self.dlg_error.content = Text(
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
					"Authorization": f"Bearer {self.basket.get('session_token')}"
				},
				json={
					"user_id": self.basket.get("id"),
					"place_id": self.place_id
				}
			)

			if response.status_code == 201:
				logger.info("Place added to favorites successfully")
				self.saved_iconbutton.icon = icons.BOOKMARK
				self.page.update()
			else:
				print("Error adding place to favorites")
				self.dlg_error.title = Text("Error al agregar")
				self.dlg_error.content = Text(
					"Ocurrió un error agregando el sitio turístico a la lista de favoritos. "
					"Favor de intentarlo de nuevo más tarde."
				)
				self.page.open(self.dlg_error)
