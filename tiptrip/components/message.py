from flet import (
	Container, Column, Text, FontWeight, border, border_radius,
	BoxShadow, Offset, padding, colors
)

from resources.config import *


class Message(Container):
	def __init__(self, is_bot: bool, message: str) -> None:
		super().__init__(
			expand=True,
			expand_loose=True,
			border_radius=border_radius.all(value=(RADIUS / 2)),
			shadow=BoxShadow(
				blur_radius=(BLUR / 2),
				offset=Offset(0, 2),
				color=colors.GREY
			),
			padding=padding.all(value=(SPACING / 2)),
			bgcolor=(
				colors.WHITE
				if is_bot
				else SECONDARY_COLOR
			),
			content=Text(
				value=message,
				color=(
					colors.BLACK
					if is_bot
					else colors.WHITE
				),
				size=MESSAGE_TEXT_SIZE
			)
		)
