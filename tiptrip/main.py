import flet as ft
from os import remove
from time import sleep
from os.path import exists, join
from logging import Logger, getLogger, basicConfig, INFO

from resources.config import *
from resources.functions import go_to_view

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
from views.place_details import PlaceDetailsView
from views.change_password import ChangePasswordView
from views.privacy_politics import PrivacyPoliticsView
from views.terms_conditions import TermsConditionsView


basicConfig(level=INFO, format=LOGGING_FORMAT)
logger: Logger = getLogger(PROJECT_NAME)


def main(page: ft.Page) -> None:
	page.title = "Tip Trip"
	page.window.width = 412
	page.window.height = 915

	logger.info(f"Starting app's basic configurations...")
	def route_change(_: ft.RouteChangeEvent) -> None:
		page.views.clear()

		# Opening view
		page.views.append(SignInView(page))
		# Other views
		match page.route:
			# Loading view
			case "/loading": page.views.append(LoadingView(page))
			# Login views
			case "/sign_in": page.views.append(SignInView(page))
			case "/sign_up": page.views.append(SignUpView(page))
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

	page.on_route_change = route_change
	page.on_view_pop = view_pop

	go_to_view(page=page, logger=logger, route="/loading")
	sleep(2.5)
	go_to_view(page=page, logger=logger, route="/sign_in")


ft.app(main, assets_dir="assets")

logger.info("Ending app execution, deleting temporal audio files if exists...")
if exists(join(TEMP_ABSPATH, TEMP_FILE_NAME)):
	remove(join(TEMP_ABSPATH, TEMP_FILE_NAME))

if exists(join(TEMP_ABSPATH, RECEIVED_TEMP_FILE_NAME)):
	remove(join(TEMP_ABSPATH, RECEIVED_TEMP_FILE_NAME))
