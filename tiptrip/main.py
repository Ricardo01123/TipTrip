from logging import basicConfig, getLogger, info, INFO
from time import sleep

from flet_route import Routing
from flet import app, Page, View, ThemeMode, RouteChangeEvent, ViewPopEvent

from resources.config import *
# from data.db import initialize_db
from resources.router import routes


basicConfig(level=INFO, format=LOGGING_FORMAT)
logger = getLogger(PROJECT_NAME)


def main(page: Page) -> None:
	info(f"Iniciando configuraciones básicas de la app...")
	page.window_width = APP_WIDTH
	page.window_height = HEIGHT_PLUS_HEADER
	page.window_resizable = False
	page.theme_mode = ThemeMode.LIGHT
	page.title = "Tip Trip"

	# logger.info(f"Iniciando base de datos...")
	# initialize_db()

	info(f"Iniciando configuraciones de navegación de la app...")
	Routing(page=page, app_routes=routes)
	# page.go("/loading")
	# sleep(1)
	# page.go("/sign_in")
	page.go(page.route)


if __name__ == "__main__":
	app(target=main)
