from flet_route import path

from views.home import HomeView
from views.sign_in import SignInView
from views.sign_up import SignUpView
from views.loading import LoadingView
from views.chatbot import ChatbotView
from views.account import AccountView
from views.place_details import PlaceDetailsView
from views.change_password import ChangePasswordView
from views.privacy_politics import PrivacyPoliticsView
from views.terms_conditions import TermsConditionsView


routes: list[path] = [
	path(
		url="/loading",
		view=LoadingView().view,
		clear=True
	),
	path(
		url="/",
		view=SignInView().view,
		clear=True
	),
	path(
		url="/change_password",
		view=ChangePasswordView().view,
		clear=True
	),
	path(
		url="/sign_up",
		view=SignUpView().view,
		clear=True
	),
	path(
		url="/privacy_politics",
		view=PrivacyPoliticsView().view,
		clear=True
	),
	path(
		url="/terms_conditions",
		view=TermsConditionsView().view,
		clear=True
	),
	path(
		url="/home",
		view=HomeView().view,
		clear=True
	),
	path(
		url="/place_details/:place_name/",
		view=PlaceDetailsView().view,
		clear=True
	),
	path(
		url="/chatbot",
		view=ChatbotView().view,
		clear=True
	),
	path(
		url="/account",
		view=AccountView().view,
		clear=True
	),
]
