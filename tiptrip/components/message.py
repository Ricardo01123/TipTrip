from flet import (
	Container, Column, Text, FontWeight, border, border_radius,
	BoxShadow, Offset, padding, colors
)

from resources.config import *


class Message(Container):
	def __init__(self, user, message):
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
				SECONDARY_COLOR
				if user != BOT_NAME
				else colors.WHITE
			),
			content=Column(
				controls=[
					Text(
						value=user,
						weight=FontWeight.BOLD,
						color=(
							colors.WHITE
							if user != BOT_NAME
							else colors.BLACK
						)
					),
					Text(
						value=message,
						color=(
							colors.WHITE
							if user != BOT_NAME
							else colors.BLACK
						)
					)
				]
			)
		)