from flet import Column, Container, Text, alignment, margin

from resources.config import PROJECT_NAME, SPACING


class MainTitleColumn(Column):
	def __init__(self, subtitle: str, top_margin: int) -> None:
		super().__init__(
			controls = [
				Container(
					margin=margin.only(top=top_margin),
					alignment=alignment.center,
					content=Text(value=PROJECT_NAME, size=30),
				),
				Container(
					alignment=alignment.center,
					content=Text(value=subtitle)
				)
			]
		)
