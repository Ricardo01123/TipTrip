import flet as ft
from logging import Logger, getLogger

from resources.config import *


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class AudioPlayer(ft.Container):
	def __init__(self, page: ft.Page, src: str, components_width: int) -> None:
		super().__init__(
			height=65,
			width=500,
			border_radius=ft.border_radius.all(value=(RADIUS / 2)),
			shadow=ft.BoxShadow(
				blur_radius=(BLUR / 2),
				offset=ft.Offset(0, 2),
				color=ft.Colors.GREY
			),
			padding=ft.padding.all(0),
			bgcolor=ft.Colors.WHITE,
		)

		self.page: ft.Page = page

		self.duration: int = 0
		self.current_position: int = 0
		self.audio: ft.Audio = ft.Audio(
			src=src,
			autoplay=False,
			volume=0.5,
			balance=0,
			on_loaded=self.on_audio_loaded,
			on_duration_changed=self.on_duration_changed,
			on_position_changed=self.on_position_changed
		)
		self.page.overlay.append(self.audio)

		self.cca_play: ft.CircleAvatar = ft.CircleAvatar(
			bgcolor=ft.Colors.WHITE,
			radius=SPACING,
			content=ft.Icon(
				name=ft.Icons.PLAY_ARROW,
				color=ft.Colors.BLACK,
				size=50
			)
		)

		self.cca_pause: ft.CircleAvatar = ft.CircleAvatar(
			bgcolor=ft.Colors.WHITE,
			radius=SPACING,
			content=ft.Icon(
				name=ft.Icons.PAUSE,
				color=ft.Colors.BLACK,
				size=50
			)
		)

		self.cont_icon: ft.Container = ft.Container(
			expand=3,
			height=65,
			width=100,
			content=self.cca_play,
			on_click=self.play_audio
		)

		self.cont_current_position: ft.Container = ft.Container(
			expand=1,
			width=400,
			alignment=ft.alignment.center_left,
			padding=ft.padding.only(left=SPACING),
			content=ft.Text("")
		)

		self.cont_duration: ft.Container = ft.Container(
			expand=1,
			width=400,
			alignment=ft.alignment.center_right,
			padding=ft.padding.only(right=SPACING),
			content=ft.Text("")
		)

		self.audio_slider: ft.Slider = ft.Slider(
			min=0,
			max=100,
			divisions=99,
			disabled=True,
			# on_change=self.on_audio_slider_change
		)

		self.content=ft.Row(
			spacing=0,
			controls=[
				self.cont_icon,
				ft.Container(
					expand=17,
					height=65,
					width=components_width,
					content=ft.Column(
						spacing=0,
						controls=[
							ft.Container(
								expand=1,
								width=components_width,
								alignment=ft.alignment.center,
								padding=ft.padding.symmetric(horizontal=(5)),
								content=self.audio_slider
							),
							ft.Container(
								expand=1,
								width=components_width,
								alignment=ft.alignment.center,
								content=ft.Row(
									spacing=0,
									alignment=ft.MainAxisAlignment.SPACE_AROUND,
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

	def on_audio_loaded(self, _: ft.ControlEvent) -> None:
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
		self.cont_duration.content = ft.Text(
			value=self.format_duration(self.duration),
			color=ft.Colors.BLACK
		)
		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()

	def on_duration_changed(self, event: ft.AudioDurationChangeEvent) -> None:
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
		self.cont_current_position.content = ft.Text("")
		self.cont_current_position.content = ft.Text(
			value=self.format_duration(self.current_position),
			color=ft.Colors.BLACK
		)

		logger.info("Updating slider value...")
		new_value: float = self.milliseconds_to_percentage(self.current_position)
		logger.info(f"New slider value: {new_value}")
		self.audio_slider.value = new_value if new_value <= 100 else 100

		logger.info("Updating icon container...")
		if self.current_position == 0:
			self.cont_icon.content = self.cca_play
			self.cont_icon.on_click = self.play_audio
		else:
			self.cont_icon.content = self.cca_pause
			self.cont_icon.on_click = self.pause_audio

		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()

	def on_position_changed(self, event: ft.AudioPositionChangeEvent) -> None:
		logger.info(f"Position changed: {event.data} milliseconds")
		self.set_current_position(int(event.data))

	# def on_audio_slider_change(self, event: ControlEvent) -> None:
	# 	logger.info(f"Slider value changed: {event.control.value}")
	# 	new_position: int = self.percentage_to_milliseconds(event.control.value)

	# 	logger.info("Seeking audio...")
	# 	self.audio.seek(new_position)

	# 	self.set_current_position(new_position)

	def play_audio(self, _: ft.ControlEvent) -> None:
		self.cont_icon.content = self.cca_pause
		self.cont_icon.on_click = self.pause_audio

		if self.current_position == 0:
			self.audio.play()
		else:
			self.audio.resume()

		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()

	def pause_audio(self, _: ft.ControlEvent) -> None:
		self.cont_icon.content = self.cca_play
		self.cont_icon.on_click = self.play_audio
		self.audio.pause()
		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()
