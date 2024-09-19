from flet import Page
from logging import Logger
from flet_route import Basket


# Navigation functions
def go_to_view(page: Page, logger: Logger, route: str) -> None:
	logger.info(f"Redirecting to view \"/{route}\"...")
	page.go(f"/{route}")


# Basket functions
def clean_basket(basket: Basket, logger: Logger) -> None:
	logger.info("Cleaning session basket...")
	basket.delete("email")
	basket.delete("session_token")
	basket.delete("username")
	basket.delete("created_at")


def format_place_name(place_name: str) -> str:
	return place_name\
			.replace(' ', "_")\
			.replace(',', "")\
			.replace('.', "")\
			.replace(':', "")\
			.replace(';', "")\
			.replace('(', "")\
			.replace(')', "")\
			.replace('Á', 'A')\
			.replace('É', 'E')\
			.replace('Í', 'I')\
			.replace('Ó', 'O')\
			.replace('Ú', 'U')\
			.replace('Ñ', 'N')\
			.replace('á', 'a')\
			.replace('é', 'e')\
			.replace('í', 'i')\
			.replace('ó', 'o')\
			.replace('ú', 'u')\
			.replace('ñ', 'n')
