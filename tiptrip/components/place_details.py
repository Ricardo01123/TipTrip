from logging import getLogger

from flet import (
	Page, Container, Row, Column, Text, Image, Icon, Stack,
	ImageFit, ImageRepeat, padding, border_radius, BoxShadow, Offset,
	ScrollMode, FontWeight, MainAxisAlignment, CrossAxisAlignment, alignment,
	colors, icons
)

from resources.config import *
from resources.functions import go_to_view


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class PlaceCard(Container):
	def __init__(
			self, page: Page, title: str, category: str, address: str,
			punctuation: int, image_name: str
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
				route=f"place_details/{title.lower().replace(' ', '_')}"
			),
			content=Row(
				expand=True,
				spacing=5,
				controls=[
					Container(
						expand=1,
						content=Column(
							spacing=(SPACING / 2),
							controls=[
								Container(
									content=Image(
										src=f"../assets/places/{image_name}",
										fit=ImageFit.FILL,
										repeat=ImageRepeat.NO_REPEAT,
										border_radius=border_radius.all(RADIUS)
									)
								),
								Container(
									content=Row(
										alignment=MainAxisAlignment.CENTER,
										spacing=3,
										controls=[
											Icon(
												name=icons.STAR,
												color=colors.AMBER,
												size=20
											)
											for _ in range(punctuation)
										]
									)
								)
							]
						)
					),
					Container(
						expand=1,
						content=Column(
							scroll=ScrollMode.HIDDEN,
							height=120,
							alignment=MainAxisAlignment.START,
							horizontal_alignment=CrossAxisAlignment.START,
							spacing=5,
							controls=[
								Container(
									content=Text(
										value=title,
										color=MAIN_COLOR,
										size=18,
										weight=FontWeight.BOLD,
									),
								),
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
													size=12
												)
											)
										]
									)
								),
								Container(content=Text(value=address))
							]
						)
					)
				]
			)
		)


class PlaceHeader(Container):
	def __init__(self, place_name: str) -> None:
		super().__init__(
			width=(APP_WIDTH - (SPACING * 3)),
			height=210,
			shadow = BoxShadow(
				blur_radius=LOW_BLUR,
				offset=Offset(0, 2),
				color=colors.GREY
			),
			content=Stack(
				controls=[
					Container(
						left=0,
						top=0,
						width=(APP_WIDTH - (SPACING * 3)),
						height=210,
						content=Image(
							src=f"../assets/places/{place_name}.jpg",
							fit=ImageFit.FILL,
							repeat=ImageRepeat.NO_REPEAT,
							border_radius=border_radius.all(value=RADIUS)
						),
					),
					Container(
						left=0,
						bottom=0,
						height=55,
						bgcolor=colors.GREY,
						opacity=0.9,
						border_radius=border_radius.all(value=RADIUS),
						content=Column(
							spacing=0,
							controls=[
								Container(
									expand=1,
									width=(APP_WIDTH - (SPACING * 3)),
									padding=padding.symmetric(
										horizontal=SPACING
									),
									alignment=alignment.center_left,
									content=Row(
										scroll=ScrollMode.HIDDEN,
										controls=[
											Text(
												value=place_name.upper(),
												size=23,
												weight=FontWeight.BOLD
											)
										]
									)
								),
								Container(
									expand=1,
									width=(APP_WIDTH - (SPACING * 3)),
									padding=padding.symmetric(
										horizontal=SPACING
									),
									content=Row(
										spacing=0,
										alignment=MainAxisAlignment.SPACE_BETWEEN,
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
																size=14
															)
														),
														Container(
															content=Text(
																value="MUSEO",
																color=SECONDARY_COLOR,
															)
														)
													]
												)
											),
											Container(
												width=40,
												bgcolor=SECONDARY_COLOR,
												border_radius=border_radius.all(
													value=(RADIUS / 2)
												),
												content=Row(
													spacing=3,
													alignment=MainAxisAlignment.CENTER,
													controls=[
														Container(
															content=Icon(
																name=icons.STAR_BORDER,
																color=colors.WHITE,
																size=14
															)
														),
														Container(
															content=Text(
																value="5",
																color=colors.WHITE
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
				]
			)
		)
