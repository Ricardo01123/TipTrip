import sqlite3 as sql

from flet import app
from flet import Page, View, ThemeMode, RouteChangeEvent, ViewPopEvent

from data.db import initialize_db
from views.home import home_view
from views.sign_in import sign_in_view
from views.sign_up import sign_up_view
from views.forgotten_pwd import forgotten_pwd_view
from resources.config import APP_WIDTH, APP_HEIGHT


def main(page: Page) -> None:
    page.window_width = APP_WIDTH
    page.window_height = APP_HEIGHT
    page.window_resizable = False
    page.theme_mode = ThemeMode.LIGHT
    page.title = "TipTrip"

    initialize_db()

    def route_change(event: RouteChangeEvent) -> None:
        page.views.clear()

        page.views.append(sign_in_view(page))

        if page.route == "/sign_up":
            page.views.append(sign_up_view(page))
        elif page.route == "/forgotten_pwd":
            page.views.append(forgotten_pwd_view(page))
        elif page.route == "/home":
            page.views.append(home_view(page))

        page.update()

    def view_pop(event: ViewPopEvent) -> None:
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    app(target=main)
