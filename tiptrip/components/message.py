from flet import *

from resources.texts import *
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
				colors.RED
				if "ERROR" in message
				else (
					colors.WHITE
					if is_bot
					else SECONDARY_COLOR
				)
			),
			content=(
				Markdown(
					value=message,
					md_style_sheet=MarkdownStyleSheet(
						p_text_style=TextStyle(
							color=colors.BLACK,
							size=MESSAGE_TEXT_SIZE
						)
					)
				)
				if is_bot else
				Text(
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
						else colors.WHITE
					),
					size=MESSAGE_TEXT_SIZE
				)
			)
		)
