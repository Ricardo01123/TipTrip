import logging
from random import choice
from flet_route import Params, Basket

from flet import (
    Page, View, Container, Column, Text, Icon,
    MainAxisAlignment, CrossAxisAlignment, TextAlign,
    BoxShadow, padding, margin, border_radius, colors, icons
)

from resources.config import *
from resources.texts import ADVICES


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


class LoadingView:
    def __init__(self):
        self.page = None
        self.params = None
        self.basket = None

    def view(self, page: Page, params: Params, basket: Basket) -> View:
        self.page = page
        self.params = params
        self.basket = basket

        return View(
            route="/loading",
            padding=padding.all(value=0.0),
            controls=[
                Container(
                    width=TOTAL_WIDTH,
                    height=(TOTAL_HEIGHT * 0.80),
                    border_radius=border_radius.only(
                        bottom_left=RADIUS,
                        bottom_right=RADIUS
                    ),
                    shadow=BoxShadow(blur_radius=BLUR),
                    bgcolor=MAIN_COLOR,
                    content=Column(
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Text(
                                value=PROJECT_NAME,
                                size=PROJECT_NAME_SIZE,
                                color=colors.WHITE
                            ),
                            Icon(
                                name=icons.FMD_GOOD_OUTLINED,
                                size=300,
                                color=colors.WHITE
                            ),
                            Text(
                                value="Cargando...",
                                size=TITLE_SIZE,
                                color=colors.WHITE
                            ),
                        ]
                    )
                ),
                Container(
                    width=TOTAL_WIDTH,
                    height=(TOTAL_HEIGHT * 0.20),
                    margin=margin.only(top=20),
                    content=Text(
                        value=f"Consejo: {choice(ADVICES)}",
                        text_align=TextAlign.CENTER
                    )
                )
            ]
        )
