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
