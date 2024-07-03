from logging import getLogger, info
from flet_route import Params, Basket

from flet import (
	Page, View, Container, ListView, Row, TextField, CircleAvatar, Icon,
	MainAxisAlignment, CrossAxisAlignment, alignment, Offset, padding,
	BoxShadow, border_radius, colors, icons, ControlEvent
)

# from data import db
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
		if self.txt_message.value:
			self.cont_icon.content = self.cca_send
			self.cont_icon.on_click = self.cca_send_clicked
		else:
			self.cont_icon.content = self.cca_mic
		self.page.update()

	def cca_send_clicked(self, event: ControlEvent) -> None:
		self.lv_chat.controls.append(
			Row(
				alignment=MainAxisAlignment.END,
				controls=[
					Container(expand=1),
					Container(
						expand=9,
						expand_loose=True,
						content=Message(
							is_bot=False,
							message=self.txt_message.value
						)
					)
				]
			)
		)

		self.lv_chat.controls.append(
			Row(
				alignment=MainAxisAlignment.START,
				controls=[
					Container(
						expand=9,
						expand_loose=True,
						content=Message(
							is_bot=True,
							message="Buscando respuesta..."
						)
					),
					Container(expand=1)
				]
			)
		)

		self.txt_message.value = ""
		self.cont_icon.content = self.cca_mic
		self.page.update()