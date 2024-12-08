import flet as ft
from logging import Logger, getLogger

from resources.config import *
from components.titles import MainTitle
from resources.functions import go_to_view
from resources.texts import TERMS_CONDITIONS
from resources.styles import cont_main_style, btn_secondary_style


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class TermsConditionsView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page

		# Custom components
		self.btn_back: ft.ElevatedButton = ft.ElevatedButton(
			width=self.page.width,
			content=ft.Text(
				value="Regresar a Registrarse",
				size=BTN_TEXT_SIZE
			),
			on_click=lambda _: go_to_view(page=self.page, logger=logger, route="/sign_up"),
			**btn_secondary_style
		)

		# View native attributes
		super().__init__(
			route="/terms_conditions",
			bgcolor=MAIN_COLOR,
			padding=ft.padding.all(value=0.0),
			controls=[
				ft.Container(
					content=ft.Column(
						controls=[
							ft.Container(
								content=ft.IconButton(
									icon=ft.Icons.ARROW_BACK,
									icon_color=ft.Colors.BLACK,
									on_click=lambda _: go_to_view(page=self.page, logger=logger, route="/sign_up"),
								)
							),
							MainTitle(
								subtitle="Términos y condiciones",
								top_margin=10
							),
							ft.Container(
								expand=True,
								content=ft.Column(
									scroll=ft.ScrollMode.HIDDEN,
									controls=[
										ft.Container(
											content=ft.Text(
												value=TERMS_CONDITIONS,
												color=ft.Colors.BLACK,
												text_align=ft.TextAlign.JUSTIFY,
												selectable=True
											)
										)
									]
								)
							),
							ft.Container(
								margin=ft.margin.only(top=SPACING),
								content=self.btn_back
							)
						]
					),
					**cont_main_style
				)
			]
		)
