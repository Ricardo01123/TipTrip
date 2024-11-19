import flet as ft
from logging import Logger, getLogger

from resources.config import *


logger: Logger = getLogger(f"{PROJECT_NAME}.carousel_component")


class Carousel(ft.Container):
	def __init__(self, page: ft.Page, items: list) -> None:
		super().__init__()
		self.page = page
		self.items: list = self.format_items(items)

		self.current_item: int = 0
		self.total_items: int = len(self.items)
		self.current_container: ft.Container = ft.Container(
			expand=True,
			content=self.items[self.current_item]
		)

		self.width = self.page.width
		self.content = ft.Row(
			alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
			vertical_alignment=ft.CrossAxisAlignment.CENTER,
			spacing=10,
			controls=[
				ft.Container(
					content=ft.Icon(
						name=ft.icons.ARROW_BACK_IOS_SHARP,
						size=25,
						color=ft.colors.BLACK
					),
					on_click=self.previus_item
				),
				self.current_container,
				ft.Container(
					content=ft.Icon(
						name=ft.icons.ARROW_FORWARD_IOS_SHARP,
						size=25,
						color=ft.colors.BLACK
					),
					on_click=self.next_item
				),
			]
		)

	def format_items(self, items: list) -> list:
		return [
			ft.Image(
				src=item,
				fit=ft.ImageFit.FILL,
				repeat=ft.ImageRepeat.NO_REPEAT,
				border_radius=ft.border_radius.all(value=RADIUS)
			)
			for item in items
		]

	def previus_item(self, _: ft.ControlEvent) -> None:
		if self.current_item == 0:
			self.current_item = self.total_items - 1
		else:
			self.current_item -= 1

		logger.info(f"Moving to item: {self.current_item}")

		self.current_container.content = self.items[self.current_item]
		logger.info(f"Current item src: {self.current_container.content.src}")
		self.page.update()

	def next_item(self, _: ft.ControlEvent) -> None:
		if self.current_item == self.total_items - 1:
			self.current_item = 0
		else:
			self.current_item += 1

		logger.info(f"Moving to item: {self.current_item}")

		self.current_container.content = self.items[self.current_item]
		logger.info(f"Current item src: {self.current_container.content.src}")
		self.page.update()
