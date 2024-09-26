import wave
from os.path import join
from pyaudio import PyAudio
from logging import getLogger
from requests import post, Response
from base64 import b64encode, b64decode

from flet_route import Params, Basket
from flet import (
	Page, View, Container, ListView, Row, TextField, CircleAvatar, Icon,
	MainAxisAlignment, CrossAxisAlignment, alignment, Offset, padding,
	BoxShadow, border_radius, colors, icons, ControlEvent
)

from resources.config import *
from components.bars import TopBar
from components.message import Message
from resources.styles import txt_messages_style


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class ChatbotView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.record_flag: bool = False

		self.txt_message: TextField = TextField(
			hint_text="Escribe un mensaje",
			on_change=self.validate,
			**txt_messages_style
		)

		self.lv_chat: ListView = ListView(
			padding=padding.all(value=SPACING),
			spacing=(SPACING / 2),
			auto_scroll=True
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
					height=RADIUS,
					bgcolor=MAIN_COLOR,
					border_radius=border_radius.only(
						bottom_left=RADIUS,
						bottom_right=RADIUS
					),
					shadow=BoxShadow(
						blur_radius=BLUR,
						color=colors.GREY_800
					),
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
			if not "ERROR" in message:
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

				logger.info("Calling the back-end agent to process the user message...")
				response: Response = post(
					url=f"{BACK_END_URL}/{AGENT_ENDPOINT}",
					headers={
						"Content-Type": "application/json",
						"Authorization": f"Bearer {self.basket.get('session_token')}"
					},
					json={
						"prompt": self.lv_chat.controls[-2].controls[1].content.content.value
					}
				)

				from time import sleep
				sleep(3)

				logger.info(f"Agent endpoint response received {response.status_code}")
				logger.info("Evaluating the agent response...")
				if response.status_code == 200:
					audio_data: str = response.json()["audio_data"]
					logger.info("Agent response is OK. Decoding audio data...")
					audio_binary = b64decode(audio_data)

					logger.info("Saving as temporary audio file...")
					with wave.open(join(TEMP_ABSPATH, RECEIVED_TEMP_FILE_NAME), "wb") as file:
						file.setnchannels(CHANNELS)
						file.setsampwidth(2)
						file.setframerate(SAMPLING_RATE)
						file.writeframes(audio_binary)

					logger.info("Replacing last agent message...")
					self.lv_chat.controls[-1].controls[0].content = Message(
						is_bot=True,
						message="Respuesta del agente",
					)
				else:
					logger.info("Agent response is NOT ok. Replacing last agent message with error message...")
					self.lv_chat.controls[-1].controls[0].content = Message(
						is_bot=True,
						message="AGENT_ERROR",
					)

		self.page.update()

	def cca_send_clicked(self, _: ControlEvent) -> None:
		logger.info("Send button clicked")
		self.add_message(is_bot=False, message=self.txt_message.value)
		self.add_message(is_bot=True, message="Buscando información...")

		logger.info("Changing components to initial state...")
		self.txt_message.value = ""
		self.cont_icon.content = self.cca_mic
		self.cont_icon.on_click = self.cca_mic_clicked
		self.page.update()

	def end_recording_auth(self) -> None:
		logger.info("Ending authorization for audio recording...")
		self.set_record_flag(False)
		self.txt_message.value = ""
		self.page.update()

	def cca_mic_clicked(self, _: ControlEvent) -> None:
		logger.info("Microphone button clicked")
		if self.record_flag:
			logger.info("Disabling authorization for audio recording...")
			self.record_flag = False
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

			logger.info("Starting audio recording...")
			frames: list = []
			while self.record_flag:
				logger.info("Listening...")
				data = stream.read(CHUNK)
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
				encoded_audio_data = b64encode(audio_file.read()).decode("utf-8")

			logger.info("Starting speech recognition...")
			response: Response = post(
				url=f"{BACK_END_URL}/{SPEECH_RECOGNITION_ENDPOINT}",
				headers={
					"Content-Type": "application/json",
					"Authorization": f"Bearer {self.basket.get('session_token')}"
				},
				json={
					"audio_data": encoded_audio_data
				}
			)

			logger.info(f"Speech recognition endpoint response received {response.status_code}: {response.json()}")
			if response.status_code == 200:
				user_message: str = response.json()["text"]
				logger.info(f"Speech captured: {user_message}")
				self.add_message(is_bot=False, message=user_message.capitalize())
			else:
				self.add_message(is_bot=False, message="SPEECH_RECOGNITION_ERROR")

			self.add_message(is_bot=True, message="Buscando información...")
			self.page.update()
