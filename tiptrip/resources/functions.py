from logging import Logger
from flet_route import Basket
from flet import Page, ControlEvent

from resources.config import MAIN_COLOR, SECONDARY_COLOR


# Navigation functions
def go_to_view(page: Page, logger: Logger, route: str) -> None:
	logger.info(f"Redirigiendo a la vista \"/{route}\"...")
	page.go(f"/{route}")


# Basket functions
def load_user_to_basket(basket: Basket, values: list) -> None:
	basket.user_id = values[0]
	basket.username = values[1]
	basket.role = values[3]


def clean_basket(basket: Basket) -> None:
	basket.user_id = ""
	basket.username = ""
	basket.role = ""


# Hover functions
def main_btn_hover(event: ControlEvent) -> None:
	event.control.bgcolor = SECONDARY_COLOR if event.data == "true" else MAIN_COLOR
	event.control.update()


def secondary_btn_hover(event: ControlEvent) -> None:
	event.control.color = SECONDARY_COLOR if event.data == "true" else MAIN_COLOR
	event.control.update()
