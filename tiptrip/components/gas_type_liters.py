from flet import (
	Page, Container, Column, RadioGroup,
	Text, TextField, Radio, InputFilter,
	MainAxisAlignment, TextAlign, colors,
	Ref
)

from resources.config import COMPONENTS_WIDTH, TEXT_SIZE
from resources.config import STATIONARY_PRICE, TANK_PRICE


class GasLitersInput(Container):
	def __init__(self, page: Page):
		super().__init__()
		self.page = page

		self.rad_gas_type: RadioGroup = RadioGroup(
			on_change=self.rad_gas_type_changed,
			content=Column(
				controls=[
					Radio(
						value="stationary",
						label=(
							"Gas estacionario "
							f"(${str(STATIONARY_PRICE)} / L)."
						),
					),
					Radio(
						value="tank",
						label=(
							"Tanque de gas "
							f"(${str(TANK_PRICE)} / L)."
						),
					),
				]
			)
		)

		self.txt_litters: TextField = TextField(
			label="Litros",
			text_align=TextAlign.LEFT,
			width=COMPONENTS_WIDTH,
			on_change=self.txt_litters_changed,
			input_filter=InputFilter(
				allow=True,
				regex_string=r"[0-9]",
				replacement_string=""
			)
		)

		self.liter_price: float = 0.0
		self.total: float = 0.0
		self.cont_total: Ref = Ref[Container]()

		self.content = Column(
			spacing=30,
			controls=[
				Container(
					content=Column(
						controls=[
							Container(
								content=Text(
									value="Seleccione un tipo de gas:",
									size=TEXT_SIZE
								)
							),
							Container(content=self.rad_gas_type)
						]
					)
				),
				Container(
					content=Column(
						controls=[
							Container(
								content=Text(
									value="Ingrese la cantidad de litros:",
									size=TEXT_SIZE
								)
							),
							Container(content=self.txt_litters),
							Container(ref=self.cont_total),
						]
					)
				)
			]
		)

	def rad_gas_type_changed(self, event) -> None:
		if self.rad_gas_type.value == "stationary":
			self.liter_price = STATIONARY_PRICE
		else:
			self.liter_price = TANK_PRICE
		self.txt_litters_changed(event)

	def txt_litters_changed(self, event) -> None:
		if self.txt_litters.value == "":
			self.total = 0.0
		else:
			self.total = float(self.txt_litters.value) * self.liter_price

		self.cont_total.current.content = Text(
			value=f"Precio total: ${self.total:.2f}",
			size=TEXT_SIZE
		)
		self.page.update()

	def get_gas_type(self) -> str:
		return self.rad_gas_type.value

	def get_liters_quantity(self) -> int:
		return (
			int(self.txt_litters.value)
			if self.txt_litters.value != ""
			else None
		)

	def get_total(self) -> float:
		return (
			float(self.total)
			if self.total != 0.0
			else None
		)
