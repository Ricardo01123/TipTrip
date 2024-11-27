import flet as ft

from resources.config import SECONDARY_COLOR


class Splash(ft.ProgressRing):
	def __init__(self, page: ft.Page) -> None:

		super().__init__(
			visible=False,
			stroke_align=0,
			left=(page.width // 2) - 20,
			top=(page.height // 2) - 20,
			tooltip="Cargando...",
			color=SECONDARY_COLOR,
		)
