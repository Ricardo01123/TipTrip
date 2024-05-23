from flet import Page, View, AppBar, Text
from flet import CrossAxisAlignment, MainAxisAlignment


def home_view(page: Page) -> View:
    return View(
        route="/home",
        controls=[
            AppBar(title=Text(value="Página principal"), bgcolor="green"),
            Text(value="Página principal", size=30)
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )
