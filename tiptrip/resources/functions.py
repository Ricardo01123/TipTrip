from logging import Logger
from flet_route import Basket
from flet import Page, ControlEvent, colors

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
