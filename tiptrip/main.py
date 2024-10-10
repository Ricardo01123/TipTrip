from time import sleep
from logging import basicConfig, getLogger, INFO

from os import remove
from os.path import exists, join

from flet import app, Page
from flet_route import Routing

from resources.config import *
from resources.router import routes


basicConfig(level=INFO, format=LOGGING_FORMAT)
logger = getLogger(PROJECT_NAME)


def main(page: Page) -> None:
	logger.info(f"Starting app's navigation configurations...")
	Routing(page=page, app_routes=routes)
	# page.go("/loading")
	# sleep(1)
	# page.go("/sign_in")
	page.go(page.route)


if __name__ == "__main__":
	app(target=main, assets_dir="assets")

	logger.info("Ending app execution, deleting temporal audio file if exists...")
	if exists(join(TEMP_ABSPATH, TEMP_FILE_NAME)):
		remove(join(TEMP_ABSPATH, TEMP_FILE_NAME))

	if exists(join(TEMP_ABSPATH, RECEIVED_TEMP_FILE_NAME)):
		remove(join(TEMP_ABSPATH, RECEIVED_TEMP_FILE_NAME))
