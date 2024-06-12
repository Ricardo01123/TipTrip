from flet import Page, Banner, TextButton, Icon, Text, ControlEvent, colors, icons


class ErrorBanner(Banner):
	def __init__(self, page: Page):
		super().__init__()
		self.page = page

		self.bgcolor = colors.RED_100
		self.leading = Icon(name=icons.ERROR, color=colors.RED_700, size=40)
		self.content = Text(value="")
		self.actions = [
			TextButton(text="Aceptar", on_click=self.close_banner)
		]

	def open_banner(self) -> None:
		self.open = True
		self.page.update()

	def close_banner(self, event: ControlEvent) -> None:
		self.open = False
		self.page.update()

	def set_content(self, text: str) -> None:
		self.content = Text(value=text)
