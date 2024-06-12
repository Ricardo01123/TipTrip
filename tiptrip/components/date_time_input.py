import logging
from datetime import datetime

from flet import (
	Page, Container, Column, Row, DatePicker, TimePicker,
	ElevatedButton, TextButton, Text, colors, icons,
	DatePickerEntryModeChangeEvent, TimePickerEntryModeChangeEvent,
	MainAxisAlignment
)

from resources.config import PROJECT_NAME, COMPONENTS_WIDTH, TEXT_SIZE


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


class DateTimeInput(Container):
	def __init__(self, page: Page):
		super().__init__()

		self.page = page
		self.now = datetime.now()

		self.deliver_date: DatePicker = DatePicker(
			first_date=datetime(self.now.year, self.now.month, self.now.day),
			last_date=datetime(self.now.year + 1, self.now.month, self.now.day),
			confirm_text="Confirmar",
			cancel_text="Cancelar",
			on_change=self.change_date,
			on_dismiss=self.deliver_date_dismissed
		)
		self.page.overlay.append(self.deliver_date)

		self.deliver_time: TimePicker = TimePicker(
			confirm_text="Confirmar",
			cancel_text="Cancelar",
			error_invalid_text="Tiempo inválido",
			help_text="Elija una hora",
			on_change=self.change_time,
			on_dismiss=self.deliver_time_dismissed
		)
		self.page.overlay.append(self.deliver_time)

		self.btn_date: ElevatedButton = ElevatedButton(
			text="Fecha",
			icon=icons.CALENDAR_MONTH,
			on_click=lambda _: self.deliver_date.pick_date(),
		)

		self.btn_time: ElevatedButton = ElevatedButton(
			text="Hora",
			icon=icons.ACCESS_TIME,
			on_click=lambda _: self.deliver_time.pick_time(),
		)

		self.content = Column(
			controls=[
				Container(
					content=Text(
						value="Seleccione la fecha y hora de envío:",
						size=TEXT_SIZE
					)
				),
				Row(
					alignment=MainAxisAlignment.SPACE_BETWEEN,
					controls=[
						Container(
							width=145,
							content=self.btn_date
						),
						Container(
							width=145,
							content=self.btn_time
						)
					]
				)
			]
		)

	def change_date(self, event: DatePickerEntryModeChangeEvent) -> None:
		message = (
			f"{self.deliver_date.value.day}/"
			f"{self.deliver_date.value.month}/"
			f"{self.deliver_date.value.year}"
		)
		logger.info(f"Date picker changed, value is {message}")
		self.btn_date.text = message
		self.page.update()

	def deliver_date_dismissed(self, event) -> None:
		logger.info("Date picker dismissed")
		logger.info(f"Date picker value: {self.deliver_date.value}")

	def change_time(self, event: TimePickerEntryModeChangeEvent) -> None:
		message = (
			f"{self.deliver_time.value.hour}:{self.deliver_time.value.minute}"
		)
		logger.info(f"Time picker changed to {message}")
		self.btn_time.text = message
		self.page.update()

	def deliver_time_dismissed(self, event) -> None:
		logger.info("Time picker dismissed")
		logger.info(f"Time picker value: {self.deliver_time.value}")

	def get_deliver_date(self) -> str:
		return(
				(
					f"{self.deliver_date.value.day}/"
					f"{self.deliver_date.value.month}/"
					f"{self.deliver_date.value.year}"
				)
				if self.deliver_date.value is not None
				else None
			)

	def get_deliver_time(self) -> str:
		return (
			f"{self.deliver_time.value.hour}:{self.deliver_time.value.minute}"
			if self.deliver_time.value is not None
			else None
		)

