from flet import (
	Container, Column,
	Text, TextField, InputFilter,
	MainAxisAlignment, TextAlign, colors
)

from resources.config import COMPONENTS_WIDTH, TEXT_SIZE


class AddressInput(Container):
	def __init__(self):
		super().__init__()

		self.txt_street: TextField = TextField(
			label="Número y calle",
			text_align=TextAlign.LEFT,
			width=COMPONENTS_WIDTH,
		)

		self.txt_colony: TextField = TextField(
			label="Colonia",
			text_align=TextAlign.LEFT,
			width=COMPONENTS_WIDTH,
		)

		self.txt_municipality: TextField = TextField(
			label="Municipio",
			text_align=TextAlign.LEFT,
			width=COMPONENTS_WIDTH,
		)

		self.txt_cp: TextField = TextField(
			label="Código postal",
			text_align=TextAlign.LEFT,
			width=COMPONENTS_WIDTH,
			input_filter=InputFilter(
				allow=True,
				regex_string=r"[0-9]",
				replacement_string=""
			)
		)

		self.txt_state: TextField = TextField(
			label="Estado o delegación",
			text_align=TextAlign.LEFT,
			width=COMPONENTS_WIDTH,
		)

		self.content = Column(
			controls=[
				Container(
					content=Text(
						value="Ingrese su dirección de envío:",
						size=TEXT_SIZE
					)
				),
				Container(self.txt_street),
				Container(self.txt_colony),
				Container(self.txt_municipality),
				Container(self.txt_cp),
				Container(self.txt_state)
			]
		)

	def get_street(self) -> str:
		return (
			self.txt_street.value
			if self.txt_street.value != ""
			else None
		)

	def get_colony(self) -> str:
		return (
			self.txt_colony.value
			if self.txt_colony.value != ""
			else None
		)

	def get_municipality(self) -> str:
		return (
			self.txt_municipality.value
			if self.txt_municipality.value != ""
			else None
		)

	def get_cp(self) -> int:
		return (
			int(self.txt_cp.value)
			if self.txt_cp.value != ""
			else None
		)

	def get_state(self) -> str:
		return (
			self.txt_state.value
			if self.txt_state.value != ""
			else None
		)
