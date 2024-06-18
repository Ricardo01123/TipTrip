from flet import Page
from logging import Logger
from flet_route import path

from views.home import HomeView
from views.sign_in import SignInView
from views.sign_up import SignUpView
from views.loading import LoadingView
from views.change_password import ChangePasswordView
from views.privacy_politics import PrivacyPoliticsView
from views.terms_conditions import TermsConditionsView


routes: list[path] = [
	path(url="/loading", clear=True, view=LoadingView().view),
	path(url="/", clear=True, view=SignInView().view),
	path(url="/change_password", clear=True, view=ChangePasswordView().view),
	path(url="/sign_up", clear=True, view=SignUpView().view),
	path(url="/privacy_politics", clear=True, view=PrivacyPoliticsView().view),
	path(url="/terms_conditions", clear=True, view=TermsConditionsView().view),
	path(url="/home", clear=True, view=HomeView().view),
]
