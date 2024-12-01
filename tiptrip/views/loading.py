import flet as ft
from random import choice

from resources.config import *
from resources.texts import ADVICES


class LoadingView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page

		# View native attributes
		super().__init__(
			route="/loading",
			bgcolor=ft.Colors.WHITE,
			padding=ft.padding.all(value=0.0),
			controls=[
				ft.Container(
					expand=8,
					width=self.page.width,
					bgcolor=MAIN_COLOR,
					padding=ft.padding.all(value=SPACING),
					border_radius=ft.border_radius.only(
						bottom_left=RADIUS,
						bottom_right=RADIUS
					),
					shadow=ft.BoxShadow(blur_radius=LOW_BLUR),
					content=ft.Column(
						alignment=ft.MainAxisAlignment.CENTER,
						horizontal_alignment=ft.CrossAxisAlignment.CENTER,
						spacing=SPACING,
						controls=[
							ft.Container(
								width=self.page.width,
								content=ft.Text(
									value=PROJECT_NAME,
									size=45,
									color=ft.Colors.WHITE,
									text_align=ft.TextAlign.CENTER
								)
							),
							ft.Container(
								width=self.page.width,
								content=ft.Icon(
									name=ft.Icons.FMD_GOOD_OUTLINED,
									size=300,
									color=ft.Colors.WHITE
								)
							),
							ft.Container(
								width=self.page.width,
								content=ft.Text(
									value="Cargando...",
									size=30,
									color=ft.Colors.WHITE,
									text_align=ft.TextAlign.CENTER
								)
							)
						]
					)
				),
				ft.Container(
					expand=2,
					width=self.page.width,
					padding=ft.padding.all(value=SPACING),
					content=ft.Text(
						value=f"Consejo: {choice(ADVICES)}",
						size=20,
						color=ft.Colors.BLACK,
						text_align=ft.TextAlign.CENTER
					)
				)
			]
		)
