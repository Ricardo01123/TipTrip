from random import choice
from flet_route import Params, Basket

from flet import (
    Page, View, Container, Column, Text, Icon, padding, margin, border_radius,
    BoxShadow, colors, icons, MainAxisAlignment, CrossAxisAlignment, TextAlign
)

from resources.config import *
from resources.texts import ADVICES


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
            bgcolor=colors.WHITE,
            padding=padding.all(value=0),
            controls=[
                Container(
                    expand=8,
                    width=self.page.width,
                    bgcolor=MAIN_COLOR,
                    padding=padding.all(value=SPACING),
                    border_radius=border_radius.only(
                        bottom_left=RADIUS,
                        bottom_right=RADIUS
                    ),
                    shadow=BoxShadow(blur_radius=LOW_BLUR),
                    content=Column(
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=SPACING,
                        controls=[
                            Container(
                                width=self.page.width,
                                content=Text(
                                    value=PROJECT_NAME,
                                    size=45,
                                    color=colors.WHITE,
                                    text_align=TextAlign.CENTER
                                )
                            ),
                            Container(
                                width=self.page.width,
                                content=Icon(
                                    name=icons.FMD_GOOD_OUTLINED,
                                    size=300,
                                    color=colors.WHITE
                                )
                            ),
                            Container(
                                width=self.page.width,
                                content=Text(
                                    value="Cargando...",
                                    size=30,
                                    color=colors.WHITE,
                                    text_align=TextAlign.CENTER
                                )
                            )
                        ]
                    )
                ),
                Container(
                    expand=2,
                    width=self.page.width,
                    padding=padding.all(value=SPACING),
                    content=Text(
                        value=f"Consejo: {choice(ADVICES)}",
                        size=20,
                        color=colors.BLACK,
                        text_align=TextAlign.CENTER
                    )
                )
            ]
        )
