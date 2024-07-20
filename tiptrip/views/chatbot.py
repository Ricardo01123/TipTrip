from logging import getLogger, info
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
	_record_flag: bool = False

	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

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

	def validate(self, event: ControlEvent) -> None:
		if self.txt_message.value == "":
			self.record_flag = True
			self.cont_icon.content = self.cca_mic
			self.cont_icon.on_click = self.cca_mic_clicked
		else:
			self.cont_icon.content = self.cca_send
			self.cont_icon.on_click = self.cca_send_clicked
		self.page.update()

	def add_message(self, is_bot: bool, message: str) -> None:
		if is_bot:
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
		else:
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

	def cca_send_clicked(self, event: ControlEvent) -> None:
		self.add_message(is_bot=False, message=self.txt_message.value)
		self.add_message(is_bot=True, message="Buscando respuesta...")

		self.txt_message.value = ""
		self.cont_icon.content = self.cca_mic
		self.cont_icon.on_click = self.cca_mic_clicked
		self.page.update()

	def end_recording_auth(self) -> None:
		logger.info("Ending authorization for audio recording...")
		self.set_record_flag(False)
		self.txt_message.value = ""
		self.page.update()


	def cca_mic_clicked(self, event: ControlEvent) -> None:
		if self.get_record_flag():
			self.end_recording_auth()
		else:
			from models.vosk_main import speech_recognition

			logger.info("Starting authorization for audio recording...")
			self.set_record_flag(True)

			logger.info("Starting speech recognition...")
			self.txt_message.value = "Grabando audio..."
			self.page.update()
			user_message: str | None = speech_recognition(logger=logger)
			self.end_recording_auth()

			logger.info(f"Speech captured: {user_message}")

			if not user_message:
				self.add_message(is_bot=False, message="ERROR")
			else:
				self.add_message(is_bot=False, message=user_message.capitalize())

			self.add_message(is_bot=True, message="Buscando respuesta...")
			self.page.update()

	@classmethod
	def get_record_flag(cls) -> bool:
		return cls._record_flag

	@classmethod
	def set_record_flag(cls, value: bool) -> None:
		cls._record_flag =  value
