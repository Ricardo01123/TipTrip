from time import sleep
from logging import basicConfig, getLogger, info, INFO

from os import remove
from os.path import exists, join

from flet import app, Page
from flet_route import Routing

from resources.router import routes
from resources.config import LOGGING_FORMAT, PROJECT_NAME, TEMP_ABSPATH, TEMP_FILE_NAME


basicConfig(level=INFO, format=LOGGING_FORMAT)
logger = getLogger(PROJECT_NAME)


def main(page: Page) -> None:
	info(f"Starting app's navigation configurations...")
	Routing(page=page, app_routes=routes)
	# page.go("/loading")
	# sleep(1)
	# page.go("/sign_in")
	page.go(page.route)


if __name__ == "__main__":
	app(target=main, assets_dir="assets")

	logger.info("Deleting temporal audio file if exists...")
	if exists(join(TEMP_ABSPATH, TEMP_FILE_NAME)):
		remove(join(TEMP_ABSPATH, TEMP_FILE_NAME))
