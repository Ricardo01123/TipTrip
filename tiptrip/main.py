import logging

from flet_route import Routing
from flet import app, Page, View, ThemeMode, RouteChangeEvent, ViewPopEvent

from data.db import initialize_db
from resources.router import routes
from resources.config import APP_WIDTH, APP_HEIGHT
from resources.config import PROJECT_NAME, LOGGING_FORMAT


logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
logger = logging.getLogger(PROJECT_NAME)


def main(page: Page) -> None:
	logger.info(f"Iniciando configuraciones básicas de la app...")
	page.window_width = APP_WIDTH
	page.window_height = APP_HEIGHT
	page.window_resizable = False
	page.theme_mode = ThemeMode.LIGHT
	page.title = "Proyecto aplicación móvil"

	logger.info(f"Iniciando base de datos...")
	initialize_db()

	logger.info(f"Iniciando configuraciones de navegación de la app...")
	Routing(page=page, app_routes=routes)
	page.go(page.route)


if __name__ == "__main__":
	app(target=main)
