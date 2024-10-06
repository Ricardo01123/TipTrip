from flet import *

from resources.config import (
	PROJECT_NAME, PROJECT_NAME_SIZE, PAGE_SUBTITLE_SIZE, SPACING
)


class MainTitle(Container):
	def __init__(self, subtitle: str, top_margin: int) -> None:
		super().__init__(
			margin=margin.only(top=top_margin),
			content=Column(
				controls=[
					Container(
						alignment=alignment.center,
						content=Text(
							value=PROJECT_NAME,
							size=PROJECT_NAME_SIZE,
							color=colors.BLACK
						),
					),
					Container(
						alignment=alignment.center,
						content=Text(
							value=subtitle,
							size=PAGE_SUBTITLE_SIZE,
							color=colors.BLACK
						)
					)
				]
			)
		)
