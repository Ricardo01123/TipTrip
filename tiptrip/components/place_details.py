from logging import getLogger

from flet import (
	Page, Container, Row, Column, Text, Image, Icon, Stack,
	ImageFit, ImageRepeat, padding, border_radius, BoxShadow, Offset,
	ScrollMode, FontWeight, MainAxisAlignment, CrossAxisAlignment, alignment,
	margin, colors, icons, ClipBehavior
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
										src=f"places/{image_name}",
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
					)
				]
			)
		)


class PlaceHeader(Container):
	def __init__(self, width: int, place_name: str) -> None:
		super().__init__(
			width=width,
			margin=margin.only(top=10),
			border_radius=border_radius.all(value=RADIUS),
			shadow = BoxShadow(
				blur_radius=LOW_BLUR,
				color=colors.BLACK
			),
			content=Stack(
				# width=width,
				clip_behavior=ClipBehavior.ANTI_ALIAS,
				controls=[
					Container(
						content=Image(
							src=f"/places/{place_name}.jpg",
							fit=ImageFit.FILL,
							repeat=ImageRepeat.NO_REPEAT,
							border_radius=border_radius.all(value=RADIUS)
						)
					),
					Container(
						bottom=0,
						# width=300,
						width=width,
						height=PLACE_DETAILS_CONT_TITLE_HEIGHT,
						clip_behavior=ClipBehavior.ANTI_ALIAS,
						bgcolor=colors.GREY,
						opacity=0.9,
						padding=padding.symmetric(
							vertical=10,
							horizontal=SPACING
						),
						border_radius=border_radius.all(value=RADIUS),
						# border_radius=border_radius.only(
						# 	bottom_left=RADIUS,
						# 	bottom_right=RADIUS
						# ),
						content=Column(
							spacing=0,
							controls=[
								Container(
									expand=1,
									bgcolor=colors.BLUE,
									alignment=alignment.center_left,
									content=Row(
										scroll=ScrollMode.HIDDEN,
										controls=[
											Text(
												value=place_name.upper().replace('_', ' '),
												color=colors.BLACK,
												weight=FontWeight.BOLD,
												size=25
											)
										]
									)
								),
								Container(
									expand=1,
									content=Row(
										spacing=0,
										alignment=MainAxisAlignment.SPACE_BETWEEN,
										controls=[
											Container(
												content=Row(
													spacing=10,
													controls=[
														Container(
															content=Icon(
																name=icons.MUSEUM_SHARP,
																color=SECONDARY_COLOR,
																size=18
															)
														),
														Container(
															content=Text(
																value="MUSEO",
																color=SECONDARY_COLOR,
																size=18
															)
														)
													]
												)
											),
											Container(
												width=80,
												bgcolor=SECONDARY_COLOR,
												border_radius=border_radius.all(
													value=15
												),
												content=Row(
													spacing=10,
													alignment=MainAxisAlignment.CENTER,
													controls=[
														Container(
															expand=1,
															alignment=alignment.center_right,
															content=Icon(
																name=icons.STAR_BORDER,
																color=colors.WHITE,
																size=18
															)
														),
														Container(
															expand=1,
															alignment=alignment.center_left,
															content=Text(
																value="5",
																color=colors.WHITE,
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
				]
			)
		)
