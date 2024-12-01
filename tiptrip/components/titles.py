import flet as ft

from resources.config import PROJECT_NAME, PROJECT_NAME_SIZE, PAGE_SUBTITLE_SIZE


class MainTitle(ft.Container):
	def __init__(self, subtitle: str, top_margin: int) -> None:
		super().__init__(
			margin=ft.margin.only(top=top_margin),
			content=ft.Column(
				controls=[
					ft.Container(
						alignment=ft.alignment.center,
						content=ft.Text(
							value=PROJECT_NAME,
							size=PROJECT_NAME_SIZE,
							color=ft.Colors.BLACK
						),
					),
					ft.Container(
						alignment=ft.alignment.center,
						content=ft.Text(
							value=subtitle,
							size=PAGE_SUBTITLE_SIZE,
							color=ft.Colors.BLACK
						)
					)
				]
			)
		)
