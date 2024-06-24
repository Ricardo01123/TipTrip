from logging import getLogger, info
from flet_route import Params, Basket

from flet import (
	Page, View, Container, Column, Text, Stack, CircleAvatar, Image, ImageFit, ImageRepeat,
	ElevatedButton, IconButton, MainAxisAlignment, alignment, Offset, FontWeight,
	padding, margin, BoxShadow, border_radius, colors, ControlEvent
)

# from data import db
from components.bars import *
from resources.config import *
from resources.functions import secondary_btn_hover, danger_btn_hover
from resources.styles import btn_secondary_style, btn_danger_style


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class AccountView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.route = None

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.route = "/account"

		return View(
			route=self.route,
			bgcolor=colors.WHITE,
			padding=padding.all(value=0.0),
			controls=[
				TopBar(page=self.page, leading=True, logger=logger),
				Container(
					expand=True,
					width=APP_WIDTH,
					content=Stack(
						controls=[
							Container(
								left=0,
								top=0,
								width=(APP_WIDTH - 16),
								height=185,
								bgcolor=MAIN_COLOR,
								content=Text(value=""),
							),
							Container(
								left=0,
								top=0,
								width=(APP_WIDTH - 16),
								height=150,
								alignment=alignment.center,
								content=Stack(
									width=(SPACING * 7),
									height=(SPACING * 7),
									controls=[
										# CircleAvatar(
										# 	radius=(SPACING * 4),
										# 	foreground_image_src="../assets/user.jpg",
										# 	background_image_src="../assets/user.jpg",
										# 	content=Text(value="FS"),
										# 	on_image_error=lambda e: print(e.data),
										# ),
										Image(
											src=f"../assets/user.jpg",
											width=(SPACING * 7),
											fit=ImageFit.CONTAIN,
											repeat=ImageRepeat.NO_REPEAT,
											border_radius=border_radius.all(
												value=(SPACING * 4)
											)
										),
										Container(
											alignment=alignment.bottom_right,
											content=CircleAvatar(
												bgcolor=SECONDARY_COLOR,
												radius=SPACING,
												content=IconButton(
													icon=icons.EDIT,
													icon_color=colors.WHITE
												)
											)
										)
									]
								)
							),
							Container(
								left=0,
								top=185 - RADIUS,
								bgcolor=colors.WHITE,
								width=(APP_WIDTH - 16),
								height=514,
								border_radius=border_radius.all(value=RADIUS),
								shadow=BoxShadow(
									blur_radius=BLUR,
									offset=Offset(0, -2),
								),
								content=Text(value="")
							),
							Container(
								left=0,
								top=210,
								width=(APP_WIDTH - 16),
								alignment=alignment.center,
								content=Column(
									width=(APP_WIDTH - (SPACING * 2)),
									alignment=MainAxisAlignment.CENTER,
									spacing=SPACING,
									controls=[
										Container(
											height=80,
											bgcolor=colors.WHITE,
											padding=padding.symmetric(
												vertical=(SPACING / 2),
												horizontal=SPACING
											),
											border_radius=border_radius.all(
												value=RADIUS
											),
											shadow=BoxShadow(
												blur_radius=LOW_BLUR,
												color=colors.GREY_500
											),
											content=Column(
												alignment=MainAxisAlignment.CENTER,
												spacing=0,
												controls=[
													Container(
														expand=1,
														width=(APP_WIDTH - (SPACING * 2)),
														alignment=alignment.bottom_left,
														content=Text(
															value="Fernanda Sandoval",
															weight=FontWeight.BOLD,
															size=20,
														),
													),
													Container(
														expand=1,
														width=(APP_WIDTH - (SPACING * 2)),
														alignment=alignment.top_left,
														content=Text(
															value="Nombre de usuario"
														),
													)
												]
											)
										),
										Container(
											height=80,
											bgcolor=colors.WHITE,
											padding=padding.symmetric(
												vertical=(SPACING / 2),
												horizontal=SPACING
											),
											border_radius=border_radius.all(
												value=RADIUS
											),
											shadow=BoxShadow(
												blur_radius=LOW_BLUR,
												color=colors.GREY_500
											),
											content=Column(
												alignment=MainAxisAlignment.CENTER,
												spacing=0,
												controls=[
													Container(
														expand=1,
														width=(APP_WIDTH - (SPACING * 2)),
														alignment=alignment.bottom_left,
														content=Text(
															value="01 de enero del 2021",
															size=18,
														),
													),
													Container(
														expand=1,
														width=(APP_WIDTH - (SPACING * 2)),
														alignment=alignment.top_left,
														content=Text(
															value="Fecha de creación de la cuenta"
														),
													)
												]
											)
										),
										Container(
											margin=margin.only(top=SPACING),
											alignment=alignment.center,
											content=ElevatedButton(
												icon=icons.EDIT,
												text="Editar perfil",
												on_hover=secondary_btn_hover,
												# on_click=self.btn_submit_clicked,
												**btn_secondary_style
											)
										),
										Container(
											alignment=alignment.center,
											content=ElevatedButton(
												icon=icons.DELETE,
												text="Eliminar cuenta",
												on_hover=danger_btn_hover,
												# on_click=self.btn_submit_clicked,
												**btn_danger_style
											)
										)
									]
								)
							),
							Container(
								left=0,
								bottom=0,
								width=(APP_WIDTH - 16),
								content=BottomBar(
									page=self.page,
									logger=logger,
									current_route=self.route
								)
							)
						]
					)
				)
			]
		)