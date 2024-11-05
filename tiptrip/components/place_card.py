from flet import *
from logging import getLogger

from resources.config import *
from resources.functions import go_to_view


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class PlaceCard(Container):
	def __init__(
			self,
			page: Page,
			id: int,
			title: str,
			category: str,
			address: str,
			punctuation: int,
			image_link: str,
			distance: float = None
		) -> None:

		super().__init__(
			bgcolor=colors.WHITE,
			padding = padding.only(
				left=(SPACING / 2),
				top=(SPACING / 2),
				right=5,
				bottom=(SPACING / 2),
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
			),
			content=Column(
				controls=[
					Container(
						content=Row(
							scroll=ScrollMode.HIDDEN,
							controls=[
								Text(
									value=title,
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
																value=category,
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
							controls=[
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
									content=Row(
										alignment=MainAxisAlignment.START,
										spacing=3,
										controls=[
											Icon(
												name=icons.STAR,
												color=colors.AMBER,
												size=20
											)
											for _ in range(int(punctuation))
										]
									) if punctuation is not None else Text(
										value="Sin puntuación",
										color=colors.RED
									)
								)
							]
						)
					)
				]
			)
		)
