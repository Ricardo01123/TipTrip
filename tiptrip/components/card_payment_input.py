from flet import (
	Container, Column,
	Text, TextField, InputFilter,
	MainAxisAlignment, TextAlign, colors
)

from resources.config import COMPONENTS_WIDTH, TEXT_SIZE


class CardPaymentInput(Container):
	def __init__(self):
		super().__init__()

		self.txt_card_number: TextField = TextField(
			label="Número de tarjeta",
			text_align=TextAlign.LEFT,
			width=COMPONENTS_WIDTH,
			input_filter=InputFilter(
				allow=True,
				regex_string=r"[0-9]",
				replacement_string=""
			)
		)

		self.txt_card_expiration_date: TextField = TextField(
			label="Fecha de vencimiento",
			text_align=TextAlign.LEFT,
			width=COMPONENTS_WIDTH,
		)

		self.txt_card_cvc: TextField = TextField(
			label="CVC",
			text_align=TextAlign.LEFT,
			width=COMPONENTS_WIDTH,
			input_filter=InputFilter(
				allow=True,
				regex_string=r"[0-9]",
				replacement_string=""
			)
		)

		self.txt_cardholder: TextField = TextField(
			label="Nombre del dueño",
			text_align=TextAlign.LEFT,
			width=COMPONENTS_WIDTH,
		)

		self.content = Column(
			controls=[
				Container(self.txt_card_number),
				Container(self.txt_card_expiration_date),
				Container(self.txt_card_cvc),
				Container(self.txt_cardholder)
			]
		)

	def get_card_number(self) -> int:
		return (
			int(self.txt_card_number.value)
			if self.txt_card_number.value != ""
			else None
		)

	def get_card_expiration_date(self) -> str:
		return (
			self.txt_card_expiration_date.value
			if self.txt_card_expiration_date.value != ""
			else None
		)

	def get_card_cvc(self) -> int:
		return (
			int(self.txt_card_cvc.value)
			if self.txt_card_cvc.value != ""
			else None
		)

	def get_cardholder(self) -> str:
		return (
			self.txt_cardholder.value
			if self.txt_cardholder.value != ""
			else None
		)
