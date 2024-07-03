from time import sleep
from logging import basicConfig, getLogger, info, INFO

from flet import app, Page
from flet_route import Routing

from resources.router import routes
from resources.config import LOGGING_FORMAT, PROJECT_NAME
# from data.db import initialize_db


basicConfig(level=INFO, format=LOGGING_FORMAT)
logger = getLogger(PROJECT_NAME)


def main(page: Page) -> None:
	# logger.info(f"Iniciando base de datos...")
	# initialize_db()

	info(f"Iniciando configuraciones de navegación de la app...")
	Routing(page=page, app_routes=routes)
	# page.go("/loading")
	# sleep(1)
	# page.go("/sign_in")
	page.go(page.route)


if __name__ == "__main__":
	app(target=main, assets_dir="assets")
