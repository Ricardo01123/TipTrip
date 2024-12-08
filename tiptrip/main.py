import logging
import flet as ft
from time import sleep
from requests import post
from os import remove, listdir
from os.path import exists, join

from resources.config import *
from resources.functions import *

from views.map import MapView
from views.home import HomeView
from views.sign_in import SignInView
from views.sign_up import SignUpView
from views.loading import LoadingView
from views.chatbot import ChatbotView
from views.account import AccountView
from views.favorites import FavoritesView
from views.update_user import UpdateUserView
from views.permission import PermissionsView
from views.verify_user import VerifyUserView
from views.place_details import PlaceDetailsView
from views.change_password import ChangePasswordView
from views.privacy_politics import PrivacyPoliticsView
from views.terms_conditions import TermsConditionsView


def main(page: ft.Page) -> None:
	page.title = PROJECT_NAME

	logger.info(f"Starting app's basic configurations...")
	def route_change(_: ft.RouteChangeEvent) -> None:
		# page.views.clear()

		# # Opening view
		# page.views.append(LoadingView(page))

		# Other views
		match page.route:
			# Loading view
			case "/loading": page.views.append(LoadingView(page))
			# Login views
			case "/sign_in": page.views.append(SignInView(page))
			case "/sign_up": page.views.append(SignUpView(page))
			case "/verify_user": page.views.append(VerifyUserView(page))
			case "/change_password": page.views.append(ChangePasswordView(page))
			case "/privacy_politics": page.views.append(PrivacyPoliticsView(page))
			case "/terms_conditions": page.views.append(TermsConditionsView(page))
			case "/permissions": page.views.append(PermissionsView(page))
			# Functionality views
			case '/': page.views.append(HomeView(page))
			case "/place_details": page.views.append(PlaceDetailsView(page))
			case "/chatbot": page.views.append(ChatbotView(page))
			case "/favorites": page.views.append(FavoritesView(page))
			case "/map": page.views.append(MapView(page))
			# User profile views
			case "/account": page.views.append(AccountView(page))
			case "/update_user": page.views.append(UpdateUserView(page))
			# Else
			case _: logger.error(f"Route '{page.route}' does not exists")

		page.update()

	def view_pop(_: ft.ViewPopEvent) -> None:
		page.views.pop()
		top_view: ft.View = page.views[-1]
		page.go(top_view.route)

	def send_log(event) -> None:
		logger.info(event)
		logger.info("Sending log to back-end...")
		#! COMMENT
		post(
			url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
			headers={"Content-Type": "application/json"},
			json={
				"user_id": 777,
				"file": encode_logfile()
			}
		)

	page.on_route_change = route_change
	page.on_view_pop = view_pop
	page.on_close = send_log
	page.on_disconnect = send_log
	page.on_error = send_log

	go_to_view(page=page, logger=logger, route="/loading")
	sleep(2.5)
	go_to_view(page=page, logger=logger, route="/sign_in")


if __name__ == "__main__":
	if not exists(join(TEMP_ABSPATH, f"{PROJECT_NAME}.log")):
		with open(join(TEMP_ABSPATH, f"{PROJECT_NAME}.log"), "w") as log_file:
			pass
	else:
		with open(join(TEMP_ABSPATH, f"{PROJECT_NAME}.log"), "r+") as log_file:
			log_file.truncate(0)

	logging.basicConfig(level=logging.INFO)
	# App loggers
	logger: logging.Logger = logging.getLogger(PROJECT_NAME)
	# .log file handler
	file_handler: logging.FileHandler = logging.FileHandler(
		filename=join(TEMP_ABSPATH, f"{PROJECT_NAME}.log")
	)
	file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
	logger.addHandler(file_handler)
	# Console handler
	console_handler: logging.StreamHandler = logging.StreamHandler()
	console_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
	logger.addHandler(console_handler)

	try:
		ft.app(main, assets_dir="assets")
	except Exception as e:
		logger.error(f"An error occurred: {e}")
	finally:
		logger.info("Sending log to back-end...")
		#! COMMENT
		post(
			url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
			headers={"Content-Type": "application/json"},
			json={
				"user_id": 777,
				"file": encode_logfile()
			}
		)

	logger.info("Ending app execution, deleting temporal audio files if exists...")
	temp_files: list[str] = [join(TEMP_ABSPATH, file) for file in listdir(TEMP_ABSPATH)]
	for file in temp_files:
		if not file.endswith(".log"):
			remove(file)
