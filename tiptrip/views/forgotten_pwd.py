import logging
from flet_route import Params, Basket
from flet import (
    Page, View, AppBar, Column, Container,
    Text, TextField, ElevatedButton, IconButton,
    MainAxisAlignment, TextAlign, padding, icons,
    ControlEvent
)

from data import db
from resources.config import *
from components.error_banner import ErrorBanner


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


class ForgottenPwdView:
    def __init__(self):
        self.page = None
        self.params = None
        self.basket = None

        self.txt_username: TextField = TextField(
            label="Nombre de usuario",
            text_align=TextAlign.LEFT,
            width=COMPONENTS_WIDTH,
            on_change=self.validate
        )
        self.txt_password: TextField = TextField(
            label="Contraseña",
            text_align=TextAlign.LEFT,
            width=COMPONENTS_WIDTH,
            disabled=True
        )
        self.btn_submit: ElevatedButton = ElevatedButton(
            text="Recuperar contraseña",
            width=COMPONENTS_WIDTH,
            disabled=True,
            on_click=self.submit
        )

    def view(self, page: Page, params: Params, basket: Basket) -> View:
        self.page = page
        self.params = params
        self.basket = basket

        self.page.banner = ErrorBanner(page)

        return View(
            route="/forgotten_pwd",
            controls=[
                AppBar(
                    title=Text(value=""),
                    leading=IconButton(
                        icon=icons.ARROW_BACK,
                        on_click=self.sign_out
                    ),
                    bgcolor="white",
                    leading_width=APP_BAR_HEIGHT
                ),
                Container(
                    width=APP_WIDTH,
                    height=APP_HEIGHT - (APP_BAR_HEIGHT * 2),
                    padding=padding.only(
                        left=EXTERIOR_PADDING,
                        right=EXTERIOR_PADDING
                    ),
                    content=Column(
                        alignment=MainAxisAlignment.SPACE_EVENLY,
                        controls=[
                            Container(
                                content=Text(
                                    value=PROJECT_NAME,
                                    size=PROJECT_NAME_SIZE
                                )
                            ),
                            Container(
                                content=Text(
                                    value="Recuperar contraseña",
                                    size=TITLE_SIZE
                                )
                            ),
                            Container(content=self.txt_username),
                            Container(content=self.txt_password),
                            Container(content=self.btn_submit)
                        ]
                    )
                )
            ]
        )

    def sign_out(self, event: ControlEvent):
        self.page.banner.close_banner(event)
        self.page.go('/')

    def validate(self, event: ControlEvent) -> None:
        self.btn_submit.disabled = False if self.txt_username.value else True
        self.page.update()

    def submit(self, event: ControlEvent) -> None:
        logger.info("Creando conexión a la base de datos...")
        connection = db.connect_to_db()

        logger.info("Verificando que el registro exista...")
        conditions = {"username": self.txt_username.value}
        record = db.get_record(connection, "users", conditions)

        if record is not None:
            logger.info("Modificando UI...")
            self.txt_password.value = record[2]
            self.txt_password.disabled = False
            self.btn_submit.disabled = True
            logger.info(
                "Contraseña de usuario \"{}\" recuperada con éxito"
                .format(self.txt_username.value)
            )
            self.page.banner.close_banner(event)

        else:
            self.page.banner.set_content("El usuario no existe")
            self.page.banner.open_banner()

        logger.info("Cerrando conexión con la base de datos...")
        db.close_connection_to_db(connection)
