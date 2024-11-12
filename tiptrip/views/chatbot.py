import wave
from flet import *
from os.path import join
from pyaudio import PyAudio
from logging import getLogger
from requests import post, Response
from base64 import b64encode, b64decode
from flet_route import Params, Basket

from resources.texts import *
from resources.config import *
from components.bars import TopBar
from components.message import Message
from components.audio_player import AudioPlayer
from resources.styles import txt_messages_style


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class ChatbotView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.record_flag: bool = False
		self.audio_players: list = []

		self.swt_audio_user: Switch = Switch(
			value=True,
			adaptive=True,
			active_color=colors.WHITE,
			active_track_color=SECONDARY_COLOR,
			on_change=self.swt_audio_user_changed
		)

		self.swt_audio_agent: Switch = Switch(
			value=True,
			adaptive=True,
			active_color=colors.WHITE,
			active_track_color=SECONDARY_COLOR,
			on_change=self.swt_audio_agent_changed
		)

		self.ext_settings: ExpansionTile = ExpansionTile(
			trailing=Icon(
				name=icons.KEYBOARD_ARROW_DOWN,
				color=colors.BLACK,
				size=22
			),
			title=Text(
				value="Configuraciones de chat",
				color=colors.BLACK,
				size=16
			),
			tile_padding=padding.symmetric(horizontal=SPACING),
			controls=[
				Container(
					padding=padding.symmetric(horizontal=SPACING),
					content=Divider(color=colors.BLACK)
				),
				ListTile(
					content_padding=padding.symmetric(horizontal=SPACING),
					title=Text(
						value="Preguntar al chatbot usando:",
						color=colors.BLACK,
						size=16
					)
				),
				Container(
					content=Row(
						alignment=MainAxisAlignment.SPACE_EVENLY,
						controls=[
							Text(
								value="Sólo texto",
								color=colors.BLACK,
								size=16
							),
							self.swt_audio_user,
							Text(
								value="Texto o audio",
								color=colors.BLACK,
								size=16
							)
						]
					)
				),
				Container(
					padding=padding.symmetric(horizontal=SPACING),
					content=Divider(color=colors.BLACK)
				),
				ListTile(
					content_padding=padding.symmetric(horizontal=SPACING),
					title=Text(
						value="Respuestas del chatbot usando:",
						color=colors.BLACK,
						size=16
					)
				),
				Container(
					content=Row(
						alignment=MainAxisAlignment.SPACE_EVENLY,
						controls=[
							Text(
								value="Texto",
								color=colors.BLACK,
								size=16
							),
							self.swt_audio_agent,
							Text(
								value="Audio",
								color=colors.BLACK,
								size=16
							)
						]
					)
				),
				Container(
					padding=padding.symmetric(horizontal=SPACING),
					content=Divider(color=colors.BLACK)
				),
				ListTile(
					content_padding=padding.only(
						top=0,
						right=SPACING,
						bottom=SPACING,
						left=SPACING
					),
					title=Text(
						value="Consideraciones a tomar en cuenta:",
						color=colors.BLACK,
						size=16
					)
				)
			]
		)

		self.txt_message: TextField = TextField(
			hint_text="Escribe un mensaje",
			on_change=self.validate,
			**txt_messages_style
		)

		self.lv_chat: ListView = ListView(
			padding=padding.all(value=SPACING),
			spacing=(SPACING / 2),
			auto_scroll=True,
			controls=[
				Row(
					alignment=MainAxisAlignment.START,
					controls=[
						Container(
							expand=9,
							expand_loose=True,
							content=Message(is_bot=True, message=AGENT_WELCOME_MESSAGE)
						),
						Container(expand=1)
					]
				)
			]
		)

		self.cca_mic: CircleAvatar = CircleAvatar(
			bgcolor=MAIN_COLOR,
			radius=SPACING,
			content=Icon(
				name=icons.MIC,
				color=colors.WHITE,
				size=25
			)
		)

		self.cca_send: CircleAvatar = CircleAvatar(
			bgcolor=MAIN_COLOR,
			radius=SPACING,
			content=Icon(
				name=icons.SEND,
				color=colors.WHITE,
				size=25
			)
		)

		self.cont_icon: Container = Container(
			expand=1,
			alignment=alignment.center_right,
			content=self.cca_mic,
			on_click=self.cca_mic_clicked
		)

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		return View(
			route="/chatbot",
			bgcolor=colors.WHITE,
			padding=padding.all(value=0.0),
			spacing=0,
			controls=[
				TopBar(page=self.page, leading=True, logger=logger),
				Container(
					width=self.page.width,
					# height=50,
					bgcolor=MAIN_COLOR,
					border_radius=border_radius.only(
						bottom_left=RADIUS,
						bottom_right=RADIUS
					),
					shadow=BoxShadow(
						blur_radius=BLUR,
						color=colors.GREY_800
					),
					content=self.ext_settings
				),
				Container(
					expand=True,
					width=self.page.width,
					content=self.lv_chat
				),
				Container(
					width=self.page.width,
					padding=padding.all(value=(SPACING / 2)),
					height=CONT_MESSAGE_HEIGHT,
					content=Row(
						alignment=MainAxisAlignment.SPACE_BETWEEN,
						vertical_alignment=CrossAxisAlignment.CENTER,
						spacing=0,
						controls=[
							Container(
								expand=5,
								height=TXT_CONT_SIZE,
								bgcolor=colors.WHITE,
								padding=padding.symmetric(
									horizontal=SPACING
								),
								border_radius=border_radius.all(
									value=RADIUS
								),
								shadow=BoxShadow(
									blur_radius=(BLUR / 2),
									offset=Offset(0, 2),
									color=colors.BLACK12
								),
								alignment=alignment.center_left,
								content=self.txt_message
							),
							self.cont_icon,
						]
					)
				)
			]
		)

	def validate(self, _: ControlEvent) -> None:
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
				Row(
					alignment=MainAxisAlignment.END,
					controls=[
						Container(expand=1),
						Container(
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
				Row(
					alignment=MainAxisAlignment.START,
					controls=[
						Container(
							expand=9,
							expand_loose=True,
							content=Message(is_bot=is_bot, message=message)
						),
						Container(expand=1)
					]
				)
			)
			self.page.update()

			if not "ERROR" in message:
				logger.info("Calling the back-end agent to process the user message...")
				# logger.info("User is asking for nearby places. Getting user location...")
				response: Response = post(
					url=f"{BACK_END_URL}/{AGENT_ENDPOINT}",
					headers={
						"Content-Type": "application/json",
						"Authorization": f"Bearer {self.basket.get('session_token')}"
					},
					json={
						"prompt": self.lv_chat.controls[-2].controls[1].content.content.value,
						"tts": self.swt_audio_agent.value,
						# "latitude": self.basket.get("latitude"),
						# "longitude": self.basket.get("longitude")
					}
				)

				logger.info("Evaluating the agent response...")
				if response.status_code == 201:
					logger.info("Agent response is OK.")

					logger.info("Checking chosen response format...")
					if not self.swt_audio_agent.value:
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
								# src=join(TEMP_ABSPATH, RECEIVED_TEMP_FILE_NAME),
								src="https://github.com/mdn/webaudio-examples/blob/main/audio-analyser/viper.mp3?raw=true",
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

	def cca_send_clicked(self, _: ControlEvent) -> None:
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

	def cca_mic_clicked(self, _: ControlEvent) -> None:
		logger.info("Microphone button clicked")
		if self.record_flag:
			logger.info("Disabling authorization for audio recording...")
			self.record_flag = False

			logger.info("Changing UI components to initial state...")
			self.txt_message.value = ""
			self.cca_mic.bgcolor = MAIN_COLOR
			self.cca_mic.content = Icon(
				name=icons.MIC,
				color=colors.WHITE,
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
			self.cca_mic.bgcolor = colors.RED
			self.cca_mic.content = Icon(
				name=icons.STOP,
				color=colors.WHITE,
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
					"Authorization": f"Bearer {self.basket.get('session_token')}"
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

	def swt_audio_user_changed(self, _: ControlEvent) -> None:
		if self.swt_audio_user.value:
			logger.info("Switch audio for user changed to Audio")
			logger.info("Changing UI components to allow audio messages...")
			self.cont_icon.content = self.cca_mic
			self.cont_icon.on_click = self.cca_mic_clicked

		else:
			logger.info("Switch audio for user changed to Text")
			logger.info("Changing UI components to allow audio messages...")
			self.cont_icon.content = self.cca_send
			self.cont_icon.on_click = self.cca_send_clicked

		self.page.update()

	def swt_audio_agent_changed(self, _: ControlEvent) -> None:
		if self.swt_audio_agent.value:
			logger.info("Switch audio for agent changed to Audio")
		else:
			logger.info("Switch audio for agent changed to Text")
