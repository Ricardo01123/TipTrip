import flet as ft

from resources.texts import *
from resources.config import *


class Message(ft.Container):
	def __init__(self, is_bot: bool, message: str) -> None:
		super().__init__(
			expand=True,
			expand_loose=True,
			border_radius=ft.border_radius.all(value=(RADIUS / 2)),
			shadow=ft.BoxShadow(
				blur_radius=(BLUR / 2),
				offset=ft.Offset(0, 2),
				color=ft.colors.GREY
			),
			padding=ft.padding.all(value=(SPACING / 2)),
			bgcolor=(
				ft.colors.RED
				if "ERROR" in message
				else (
					ft.colors.WHITE
					if is_bot
					else SECONDARY_COLOR
				)
			),
			content=(
				ft.Markdown(
					value=message,
					md_style_sheet=ft.MarkdownStyleSheet(
						p_text_style=ft.TextStyle(
							color=ft.colors.BLACK,
							size=MESSAGE_TEXT_SIZE
						)
					)
				)
				if is_bot else
				ft.Text(
					value=(
						message
						if "ERROR" not in message
						else (
							SPEECH_RECOGNITION_ERROR_MESSAGE
							if message == "SPEECH_RECOGNITION_ERROR"
							else AGENT_ERROR_MESSAGE
						)
					),
					color=(
						colors.BLACK
						if is_bot and "ERROR" not in message
						else ft.colors.WHITE
					),
					size=MESSAGE_TEXT_SIZE
				)
			)
		)
