from flet import *
from logging import getLogger

from resources.config import *


logger = getLogger(f"{PROJECT_NAME}.carousel_component")


class Carousel(Container):
	def __init__(self, page: Page, items: list) -> None:
		super().__init__()
		self.page = page
		self.items = self.format_items(items)

		self.current_item: int = 0
		self.total_items: int = len(self.items)
		self.current_container: Container = Container(
			expand=True,
			content=self.items[self.current_item]
		)

		self.width = self.page.width
		self.content = Row(
			alignment=MainAxisAlignment.SPACE_BETWEEN,
			vertical_alignment=CrossAxisAlignment.CENTER,
			spacing=10,
			controls=[
				Container(
					content=Icon(
						name=icons.ARROW_BACK_IOS_SHARP,
						size=25,
						color=colors.BLACK
					),
					on_click=self.previus_item
				),
				self.current_container,
				Container(
					content=Icon(
						name=icons.ARROW_FORWARD_IOS_SHARP,
						size=25,
						color=colors.BLACK
					),
					on_click=self.next_item
				),
			]
		)

	def format_items(self, items: list) -> list:
		return [
			Image(
				# src=f"/places/{item}",
				src=item,
				fit=ImageFit.FILL,
				repeat=ImageRepeat.NO_REPEAT,
				border_radius=border_radius.all(value=RADIUS)
			)
			for item in items
		]

	def previus_item(self, _: ControlEvent) -> None:
		if self.current_item == 0:
			self.current_item = self.total_items - 1
		else:
			self.current_item -= 1

		logger.info(f"Moving to item: {self.current_item}")

		self.current_container.content = self.items[self.current_item]
		logger.info(f"Current item src: {self.current_container.content.src}")
		self.page.update()

	def next_item(self, _: ControlEvent) -> None:
		if self.current_item == self.total_items - 1:
			self.current_item = 0
		else:
			self.current_item += 1

		logger.info(f"Moving to item: {self.current_item}")

		self.current_container.content = self.items[self.current_item]
		logger.info(f"Current item src: {self.current_container.content.src}")
		self.page.update()
