from flet import Page, View
from flet_route import path

from resources.config import PROJECT_NAME

from views.home import HomeView
from views.paid import PaidView
from views.sign_in import SignInView
from views.sign_up import SignUpView
from views.history_view import HistoryView
from views.forgotten_pwd import ForgottenPwdView


routes: list = [
	path(url='/', clear=True, view=SignInView().view),
	path(url="/home/:username", clear=True, view=HomeView().view),
	path(url="/sign_in", clear=True, view=SignInView().view),
	path(url="/sign_up", clear=True, view=SignUpView().view),
	path(url="/forgotten_pwd", clear=True, view=ForgottenPwdView().view),
	path(url="/paid/:last_order_id", clear=True, view=PaidView().view),
	path(url="/history", clear=True, view=HistoryView().view)
]
