import wave
import flet as ft
from os.path import join
from pyaudio import PyAudio
from requests import post, Response
from logging import Logger, getLogger
from base64 import b64encode, b64decode

from resources.texts import *
from resources.config import *
from components.bars import TopBar
from components.message import Message
from components.audio_player import AudioPlayer
from resources.styles import txt_messages_style


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class ChatbotView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page
		self.record_flag: bool = False
		self.audio_players: list = []

		# Custom components
		# Settings components
		self.swt_audio: ft.Switch = ft.Switch(
			value=True,
			adaptive=True,
			active_color=ft.colors.WHITE,
			active_track_color=SECONDARY_COLOR,
			on_change=self.swt_audio_changed
		)
		self.ext_settings: ft.ExpansionTile = ft.ExpansionTile(
			trailing=ft.Icon(
				name=ft.icons.KEYBOARD_ARROW_DOWN,
				color=ft.colors.BLACK,
				size=22
			),
			title=ft.Text(
				value="Configuraciones de chat",
				color=ft.colors.BLACK,
				size=16
			),
			tile_padding=ft.padding.symmetric(horizontal=SPACING),
			controls=[
				ft.ListTile(
					content_padding=ft.padding.symmetric(horizontal=SPACING),
					title=ft.Text(
						value="Respuestas del chatbot usando:",
						color=ft.colors.BLACK,
						size=16
					)
				),
				ft.Container(
					content=ft.Row(
						alignment=ft.MainAxisAlignment.SPACE_EVENLY,
						controls=[
							ft.Text(
								value="Texto",
								color=ft.colors.BLACK,
								size=16
							),
							self.swt_audio,
							ft.Text(
								value="Audio",
								color=ft.colors.BLACK,
								size=16
							)
						]
					)
				)
			]
		)

		# ListView (Chat) components
		self.txt_message: ft.TextField = ft.TextField(
			hint_text="Escribe un mensaje",
			on_change=self.validate,
			**txt_messages_style
		)
		self.lv_chat: ft.ListView = ft.ListView(
			padding=ft.padding.all(value=SPACING),
			spacing=(SPACING / 2),
			auto_scroll=True,
			controls=[
				ft.Row(
					alignment=ft.MainAxisAlignment.START,
					controls=[
						ft.Container(
							expand=9,
							expand_loose=True,
							content=Message(is_bot=True, message=AGENT_WELCOME_MESSAGE)
						),
						ft.Container(expand=1)
					]
				)
			]
		)
		self.cca_mic: ft.CircleAvatar = ft.CircleAvatar(
			bgcolor=MAIN_COLOR,
			radius=SPACING,
			content=ft.Icon(
				name=ft.icons.MIC,
				color=ft.colors.WHITE,
				size=25
			)
		)
		self.cca_send: ft.CircleAvatar = ft.CircleAvatar(
			bgcolor=MAIN_COLOR,
			radius=SPACING,
			content=ft.Icon(
				name=ft.icons.SEND,
				color=ft.colors.WHITE,
				size=25
			)
		)
		self.cont_icon: ft.Container = ft.Container(
			expand=1,
			alignment=ft.alignment.center_right,
			content=self.cca_mic,
			on_click=self.cca_mic_clicked
		)

		# View native attributes
		super().__init__(
			route="/chatbot",
			bgcolor=ft.colors.WHITE,
			padding=ft.padding.all(value=0.0),
			spacing=0,
			controls=[
				TopBar(page=self.page, leading=True, logger=logger),
				ft.Container(
					width=self.page.width,
					# height=50,
					bgcolor=MAIN_COLOR,
					border_radius=ft.border_radius.only(
						bottom_left=RADIUS,
						bottom_right=RADIUS
					),
					shadow=ft.BoxShadow(
						blur_radius=BLUR,
						color=ft.colors.GREY_800
					),
					content=self.ext_settings
				),
				ft.Container(
					expand=True,
					width=self.page.width,
					content=self.lv_chat
				),
				ft.Container(
					width=self.page.width,
					padding=ft.padding.all(value=(SPACING / 2)),
					height=CONT_MESSAGE_HEIGHT,
					content=ft.Row(
						alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
						vertical_alignment=ft.CrossAxisAlignment.CENTER,
						spacing=0,
						controls=[
							ft.Container(
								expand=5,
								height=TXT_CONT_SIZE,
								bgcolor=ft.colors.WHITE,
								padding=ft.padding.symmetric(
									horizontal=SPACING
								),
								border_radius=ft.border_radius.all(
									value=RADIUS
								),
								shadow=ft.BoxShadow(
									blur_radius=(BLUR / 2),
									offset=ft.Offset(0, 2),
									color=ft.colors.BLACK12
								),
								alignment=ft.alignment.center_left,
								content=self.txt_message
							),
							self.cont_icon,
						]
					)
				)
			]
		)

	def validate(self, _: ft.ControlEvent) -> None:
		if self.txt_message.value == "":
			self.record_flag = True
			self.cont_icon.content = self.cca_mic
			self.cont_icon.on_click = self.cca_mic_clicked
		else:
			self.cont_icon.content = self.cca_send
			self.cont_icon.on_click = self.cca_send_clicked
		self.page.update()

	def add_message(self, is_bot: bool, message: str) -> None:
		if not is_bot:
			logger.info("Adding user message...")
			self.lv_chat.controls.append(
				ft.Row(
					alignment=ft.MainAxisAlignment.END,
					controls=[
						ft.Container(expand=1),
						ft.Container(
							expand=9,
							expand_loose=True,
							content=Message(is_bot=is_bot, message=message)
						)
					]
				)
			)
		else:
			logger.info("Adding agent message while process the user message...")
			self.lv_chat.controls.append(
				ft.Row(
					alignment=ft.MainAxisAlignment.START,
					controls=[
						ft.Container(
							expand=9,
							expand_loose=True,
							content=Message(is_bot=is_bot, message=message)
						),
						ft.Container(expand=1)
					]
				)
			)
			self.page.update()

			if not "ERROR" in message:
				logger.info("Calling the back-end agent to process the user message...")
				# logger.info("User is asking for nearby places. Getting user location...")
				response: Response = post(
					url=f"{BACK_END_URL}/{AGENT_ENDPOINT}/{self.page.session.get('id')}",
					headers={
						"Content-Type": "application/json",
						"Authorization": f"Bearer {self.page.session.get('session_token')}"
					},
					json={
						"prompt": self.lv_chat.controls[-2].controls[1].content.content.value,
						"tts": self.swt_audio.value,
						# "latitude": self.page.session.get("latitude"),
						# "longitude": self.page.session.get("longitude")
					}
				)

				logger.info("Evaluating the agent response...")
				if response.status_code == 201:
					logger.info("Agent response is OK.")

					logger.info("Checking chosen response format...")
					if not self.swt_audio.value:
						logger.info("Agent response is only text")
						logger.info("Replacing last agent message with agent response message...")
						self.lv_chat.controls[-1].controls[0].content = Message(
							is_bot=True,
							message=response.json()["agent_response"]["text"],
						)

					else:
						logger.info("Agent response is audio messages")
						data: dict = response.json()
						logger.info(f"Agent text response: \"{data['agent_response']['text']}\"")

						logger.info("Getting audio data from agent response...")
						audio_data: dict = response.json()["agent_response"]["audio_data"]

						logger.info("Decoding audio data...")
						audio_binary = b64decode(audio_data["audio"])

						logger.info("Saving as temporary audio file...")
						with wave.open(join(TEMP_ABSPATH, RECEIVED_TEMP_FILE_NAME), "wb") as file:
							file.setnchannels(audio_data["nchannels"])
							file.setsampwidth(audio_data["sampwidth"])
							file.setframerate(audio_data["framerate"])
							file.setnframes(audio_data["nframes"])
							# file.setcomptype(audio_data["comp_type"])
							# file.setcompname(audio_data["comp_name"])
							file.writeframes(audio_binary)

						logger.info("Creating new AudioPlayer component and waiting for audio to be loaded...")
						self.audio_players.append(
							AudioPlayer(
								page=self.page,
								src=join(TEMP_ABSPATH, RECEIVED_TEMP_FILE_NAME),
								components_width=self.page.width
							)
						)

						logger.info("Replacing last agent message...")
						self.lv_chat.controls[-1].controls[0].content = self.audio_players[-1]

				else:
					logger.info(f"Agent endpoint response received {response.status_code}: {response.json()}")
					logger.info("Agent response is NOT ok. Replacing last agent message with error message...")
					self.lv_chat.controls[-1].controls[0].content = Message(
						is_bot=True,
						message="AGENT_ERROR",
					)

		logger.info("Updating live view components...")
		self.lv_chat.update()

	def cca_send_clicked(self, _: ft.ControlEvent) -> None:
		if self.txt_message.value == "" or self.txt_message.value.isspace():
			logger.info("Empty message, not sending...")

		else:
			logger.info("Send button clicked")

			logger.info("Changing components to initial state...")
			aux_message: str = self.txt_message.value
			self.txt_message.value = ""
			self.cont_icon.content = self.cca_mic
			self.cont_icon.on_click = self.cca_mic_clicked
			self.page.update()

			self.add_message(is_bot=False, message=aux_message)
			self.add_message(is_bot=True, message="Buscando información...")

	def cca_mic_clicked(self, _: ft.ControlEvent) -> None:
		logger.info("Microphone button clicked")
		if self.record_flag:
			logger.info("Disabling authorization for audio recording...")
			self.record_flag = False

			logger.info("Changing UI components to initial state...")
			self.txt_message.value = ""
			self.cca_mic.bgcolor = MAIN_COLOR
			self.cca_mic.content = ft.Icon(
				name=ft.icons.MIC,
				color=ft.colors.WHITE,
				size=25
			)
			self.page.update()
		else:
			logger.info("Establishing audio configuration...")
			audio: PyAudio = PyAudio()
			stream = audio.open(
				format=FORMAT,
				channels=CHANNELS,
				rate=SAMPLING_RATE,
				input=True,
				frames_per_buffer=CHUNK
			)

			logger.info("Establishing authorization for audio recording...")
			self.record_flag = True

			logger.info("Changing UI components to recording state...")
			self.txt_message.value = "Grabando audio..."
			self.cca_mic.bgcolor = ft.colors.RED
			self.cca_mic.content = ft.Icon(
				name=ft.icons.STOP,
				color=ft.colors.WHITE,
				size=25
			)
			self.page.update()

			logger.info("Starting audio recording...")
			frames: list = []
			while self.record_flag:
				logger.info("Listening...")
				data: bytes = stream.read(CHUNK)
				frames.append(data)

			logger.info("Ending audio recording...")
			stream.stop_stream()
			stream.close()
			audio.terminate()

			logger.info("Saving audio file...")
			with wave.open(join(TEMP_ABSPATH, TEMP_FILE_NAME), "wb") as file:
				file.setnchannels(CHANNELS)
				file.setsampwidth(audio.get_sample_size(FORMAT))
				file.setframerate(SAMPLING_RATE)
				file.writeframes(b"".join(frames))

			logger.info("Encoding audio file...")
			with open(join(TEMP_ABSPATH, TEMP_FILE_NAME), "rb") as audio_file:
				encoded_audio_data: str = b64encode(audio_file.read()).decode("utf-8")

			logger.info("Calling Backend API for speech recognition...")
			response: Response = post(
				url=f"{BACK_END_URL}/{ASR_ENDPOINT}",
				headers={
					"Content-Type": "application/json",
					"Authorization": f"Bearer {self.page.session.get('session_token')}"
				},
				json={
					"audio": encoded_audio_data
				}
			)

			logger.info(f"Speech recognition (ASR) endpoint response received {response.status_code}: {response.json()}")
			if response.status_code == 201:
				user_message: str = response.json()["text"]
				logger.info(f"Speech captured: {user_message}")
				self.add_message(is_bot=False, message=user_message.capitalize())

				logger.info("Adding agent message...")
				self.add_message(is_bot=True, message="Buscando información...")
				self.page.update()

			else:
				self.add_message(is_bot=False, message="SPEECH_RECOGNITION_ERROR")

	def swt_audio_changed(self, _: ft.ControlEvent) -> None:
		if self.swt_audio.value:
			logger.info("Switch audio for agent changed to Audio")
		else:
			logger.info("Switch audio for agent changed to Text")
