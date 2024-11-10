from time import sleep
from logging import basicConfig, getLogger, INFO

from os import remove
from os.path import exists, join

from flet import *
from flet_route import Routing

from resources.config import *
from resources.router import routes
# from components.loading_ring import loading_ring


basicConfig(level=INFO, format=LOGGING_FORMAT)
logger = getLogger(PROJECT_NAME)


def main(page: Page) -> None:
	logger.info(f"Starting app's navigation configurations...")
	page.window.width = 412
	page.window.height = 915
	# loading_ring.left = (page.window.width // 2) - (LOADING_RING_SIZE // 2)
	# loading_ring.top = (page.window.height // 2) - (LOADING_RING_SIZE // 2)
	# page.overlay.append(loading_ring)

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
