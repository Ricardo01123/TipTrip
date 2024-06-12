from flet_route import Basket


def load_user_to_basket(basket: Basket, values: list) -> None:
	basket.user_id = values[0]
	basket.username = values[1]
	basket.role = values[3]


def clean_basket(basket: Basket) -> None:
	basket.user_id = ""
	basket.username = ""
	basket.role = ""
