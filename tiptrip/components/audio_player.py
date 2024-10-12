from flet import *
from logging import getLogger

from resources.config import *


logger = getLogger(f"{PROJECT_NAME}.audio_player_component")


class AudioPlayer(Container):
	def __init__(self, page: Page, src: str, components_width: int) -> None:
		super().__init__(
			height=65,
			width=500,
			border_radius=border_radius.all(value=(RADIUS / 2)),
			shadow=BoxShadow(
				blur_radius=(BLUR / 2),
				offset=Offset(0, 2),
				color=colors.GREY
			),
			padding=padding.all(0),
			bgcolor=colors.WHITE,
		)

		self.page = page

		self.duration: int = 0
		self.current_position: int = 0
		self.audio: Audio = Audio(
			src=src,
			autoplay=False,
			volume=0.5,
			balance=0,
			on_loaded=self.on_audio_loaded,
			on_duration_changed=self.on_duration_changed,
			on_position_changed=self.on_position_changed
		)
		self.page.overlay.append(self.audio)

		self.cca_play: CircleAvatar = CircleAvatar(
			bgcolor=colors.WHITE,
			radius=SPACING,
			content=Icon(
				name=icons.PLAY_ARROW,
				color=colors.BLACK,
				size=50
			)
		)

		self.cca_pause: CircleAvatar = CircleAvatar(
			bgcolor=colors.WHITE,
			radius=SPACING,
			content=Icon(
				name=icons.PAUSE,
				color=colors.BLACK,
				size=50
			)
		)

		self.cont_icon: Container = Container(
			expand=3,
			height=65,
			width=100,
			content=self.cca_play,
			on_click=self.play_audio
		)

		self.cont_current_position: Container = Container(
			expand=1,
			width=400,
			alignment=alignment.center_left,
			padding=padding.only(left=SPACING),
			content=Text("")
		)

		self.cont_duration: Container = Container(
			expand=1,
			width=400,
			alignment=alignment.center_right,
			padding=padding.only(right=SPACING),
			content=Text("")
		)

		self.audio_slider: Slider = Slider(
			min=0,
			max=100,
			divisions=99,
			disabled=True,
			# on_change=self.on_audio_slider_change
		)

		self.content=Row(
			spacing=0,
			controls=[
				self.cont_icon,
				Container(
					expand=17,
					height=65,
					width=components_width,
					content=Column(
						spacing=0,
						controls=[
							Container(
								expand=1,
								width=components_width,
								alignment=alignment.center,
								padding=padding.symmetric(horizontal=(5)),
								content=self.audio_slider
							),
							Container(
								expand=1,
								width=components_width,
								alignment=alignment.center,
								content=Row(
									spacing=0,
									alignment=MainAxisAlignment.SPACE_AROUND,
									controls=[
										self.cont_current_position,
										self.cont_duration
									]
								)
							)
						]
					)
				)
			]
		)

	def on_audio_loaded(self, _: ControlEvent) -> None:
		logger.info("Audio loaded successfully")
		logger.info("Setting duration and position parameters...")

	def format_duration(self, milliseconds: int) -> str:
		total_seconds: int = milliseconds // 1000
		minutes: int = total_seconds // 60
		seconds: int = total_seconds % 60
		return f"{minutes:02}:{seconds:02}"

	def set_duration(self, duration: int) -> None:
		logger.info(f"New duration: {duration} milliseconds")
		self.duration = duration

		logger.info("Updating duration text container...")
		self.cont_duration.content = Text(
			value=self.format_duration(self.duration),
			color=colors.BLACK
		)
		self.page.update()

	def on_duration_changed(self, event: AudioDurationChangeEvent) -> None:
		self.set_duration(int(event.data))

	def milliseconds_to_percentage(self, milliseconds: int) -> float:
		if self.duration == 0:
			return 0
		return (milliseconds / self.duration) * 100

	# def percentage_to_milliseconds(self, percentage: float) -> int:
	# 	return (percentage / 100) * self.duration

	def set_current_position(self, position: int) -> None:
		logger.info(f"New current position: {position} milliseconds")
		self.current_position = position

		logger.info("Updating current position text container...")
		self.cont_current_position.content = Text("")
		self.cont_current_position.content = Text(
			value=self.format_duration(self.current_position),
			color=colors.BLACK
		)

		logger.info("Updating slider value...")
		self.audio_slider.value = self.milliseconds_to_percentage(self.current_position)
		logger.info(f"New slider value: {self.audio_slider.value}")

		if self.current_position == 0:
			logger.info("Audio finished. Resetting play icon...")
			self.cont_icon.content = self.cca_play
			self.cont_icon.on_click = self.play_audio

		self.page.update()

	def on_position_changed(self, event: AudioPositionChangeEvent) -> None:
		logger.info(f"Position changed: {event.data} milliseconds")
		self.set_current_position(int(event.data))

	# def on_audio_slider_change(self, event: ControlEvent) -> None:
	# 	logger.info(f"Slider value changed: {event.control.value}")
	# 	new_position: int = self.percentage_to_milliseconds(event.control.value)

	# 	logger.info("Seeking audio...")
	# 	self.audio.seek(new_position)

	# 	self.set_current_position(new_position)

	def play_audio(self, _: ControlEvent) -> None:
		self.cont_icon.content = self.cca_pause
		self.cont_icon.on_click = self.pause_audio

		if self.current_position == 0:
			self.audio.play()
		else:
			self.audio.resume()

		self.page.update()

	def pause_audio(self, _: ControlEvent) -> None:
		self.cont_icon.content = self.cca_play
		self.cont_icon.on_click = self.play_audio
		self.audio.pause()
		self.page.update()
