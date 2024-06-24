from logging import getLogger, info
from flet_route import Params, Basket

from flet import (
	Page, View, Container, ListView, Column, Row, Text, TextField, CircleAvatar,
	Icon, Stack, MainAxisAlignment, CrossAxisAlignment, alignment, Offset,
	LinearGradient, padding, BoxShadow, InputBorder, border_radius,
	colors, icons, ControlEvent
)

# from data import db
from resources.config import *
from components.bars import TopBar
from components.message import Message


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class ChatbotView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.txt_message: TextField = TextField(
			label=None,
			hint_text="Escribe un mensaje",
			border=InputBorder.NONE,
			cursor_color=SECONDARY_COLOR,
			on_change=self.validate
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
				color=colors.WHITE
			)
		)

		self.cca_send: CircleAvatar = CircleAvatar(
			bgcolor=MAIN_COLOR,
			radius=SPACING,
			content=Icon(
				name=icons.SEND,
				color=colors.WHITE
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
			controls=[
				TopBar(page=self.page, leading=True, logger=logger),
				Container(
					expand=True,
					width=APP_WIDTH,
					content=Stack(
						controls=[
							Container(
								left=0,
								top=0,
								width=(APP_WIDTH - 16),
								height=30,
								bgcolor=MAIN_COLOR,
								border_radius=border_radius.only(
									bottom_left=RADIUS,
									bottom_right=RADIUS
								),
								shadow=BoxShadow(
									blur_radius=BLUR,
									color=colors.GREY_800
								),
								content=Text(value=""),
							),
							Container(
								left=0,
								top=30,
								width=(APP_WIDTH - 16),
								height=544,
								content=self.lv_chat
							),
							Container(
								left=0,
								bottom=(SPACING / 2),
								width=(APP_WIDTH - 16),
								height=45,
								alignment=alignment.center,
								content=Row(
									width=(APP_WIDTH - (SPACING * 2)),
									alignment=MainAxisAlignment.SPACE_BETWEEN,
									vertical_alignment=CrossAxisAlignment.CENTER,
									spacing=0,
									controls=[
										Container(
											expand=5,
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
											content=self.txt_message
										),
										self.cont_icon,
									],
								)
							)
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
					Message(
						user="Fernanda",
						message=self.txt_message.value
					)
				]
			)
		)

		self.lv_chat.controls.append(
			Row(
				alignment=MainAxisAlignment.START,
				controls=[
					Message(
						user="Bot",
						message="Buscando respuesta..."
					)
				]
			)
		)

		self.txt_message.value = ""
		self.cont_icon.content = self.cca_mic
		self.page.update()