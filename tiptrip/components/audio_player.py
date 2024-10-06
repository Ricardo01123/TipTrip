from flet import *
from logging import getLogger

from resources.config import *


logger = getLogger(f"{PROJECT_NAME}.audio_player_component")


class AudioPlayer(Container):
	def __init__(self, page: Page, audio_base64: str) -> None:
		super().__init__(
			height=65,
			border_radius=border_radius.all(value=(RADIUS / 2)),
			shadow=BoxShadow(
				blur_radius=(BLUR / 2),
				offset=Offset(0, 2),
				color=colors.GREY
			),
			padding=padding.all(value=(SPACING / 2)),
			bgcolor=colors.WHITE,
		)

		self.page = page
		self.duration: int = 0

		self.cca_play: CircleAvatar = CircleAvatar(
			bgcolor=MAIN_COLOR,
			radius=SPACING,
			content=Icon(
				name=icons.PLAY_ARROW,
				color=colors.WHITE,
				size=40
			)
		)

		self.cca_pause: CircleAvatar = CircleAvatar(
			bgcolor=MAIN_COLOR,
			radius=SPACING,
			content=Icon(
				name=icons.PAUSE,
				color=colors.WHITE,
				size=40
			)
		)

		self.cont_icon: Container = Container(
			expand=1,
			alignment=alignment.center_right,
			content=self.cca_play,
			on_click=self.play_audio
		)

		self.audio = Audio(
			src_base64=audio_base64,
			autoplay=False,
			volume=0.5,
			balance=0,
			on_loaded=lambda _: logger.debug("Audio loaded successfully"),
			on_duration_changed=self.set_duration,
			on_position_changed=self.handle_audio_position_changed,
			on_state_changed=lambda e: print("State changed: {e.data}"),
		)
		self.page.overlay.append(self.audio)

		self.sld_audio_position: Slider = Slider(
			min=0,
			max=5,
			divisions=5,
			value=1,
			disabled=True
		)

		self.content = Row(
			alignment=MainAxisAlignment.SPACE_EVENLY,
			vertical_alignment=CrossAxisAlignment.CENTER,
			spacing=10,
			controls=[
				Container(
					# expand=2,
					content=Icon(
						name=icons.PLAY_ARROW,
						size=30,
						color=colors.BLACK
					),
					# on_click=self.play_audio
				),
				Container(
					# expand=8,
					expand_loose=True,
					content=Column(
						controls=[
							Container(
								expand=1,
								content=self.sld_audio_position
							),
							Container(
								expand=1,
								content=Row(
									alignment=MainAxisAlignment.SPACE_BETWEEN,
									controls=[
										Container(
											expand=1,
											content=Text(
												value="00:00",
												color=colors.BLACK
											)
										),
										Container(
											expand=1,
											content=Text(
												# value=f"{self.duration}",
												value="00:00",
												color=colors.BLACK
											)
										),
									]
								)
							)
						]
					)
				)
			]
		)

	def set_duration(self, event) -> None:
		logger.info(f"Audio duration changed: {event.data}")
		self.duration = event.data

	def handle_audio_position_changed(self, e) -> None:
		logger.info(f"Audio position changed: {e.data}")
		# self.sld_audio_position.value = (e.data / self.duration) * 100

	def play_audio(self, _) -> None:
		self.audio.play()
		self.cont_icon.content = self.cca_pause
		self.cont_icon.on_click = self.pause_audio
		self.page.update()

	def pause_audio(self, _) -> None:
		self.audio.pause()
		self.cont_icon.content = self.cca_play
		self.cont_icon.on_click = self.play_audio
		self.page.update()
