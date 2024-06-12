import logging

from flet import (
	Page, Container, Column, RadioGroup,
	Text, Radio, colors
)

from .card_payment_input import CardPaymentInput
from resources.config import PROJECT_NAME, TEXT_SIZE


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


class PaymentInput(Container):
	def __init__(self, page: Page):
		super().__init__()

		self.page = page

		self.card_payment_input = CardPaymentInput()
		self.card_payment_input.visible = False

		self.rad_payment: RadioGroup = RadioGroup(
			on_change=self.rad_payment_changed,
			content=Column(
				controls=[
					Radio(
						value="cash",
						label="Efectivo",
					),
					Radio(
						value="card",
						label="Tarjeta de crédito/débito",
					)
				]
			)
		)

		self.content = Column(
			controls=[
				Container(
					content=Text(
						value="Seleccione su método de pago:",
						size=TEXT_SIZE
					)
				),
				Container(content=self.rad_payment),
				Container(content=self.card_payment_input),
			]
		)

	def rad_payment_changed(self, event) -> None:
		if self.rad_payment.value == "cash":
			self.card_payment_input.visible = False
		else:
			self.card_payment_input.visible = True
		self.page.update()

	def get_payment_method(self) -> str:
		return self.rad_payment.value
