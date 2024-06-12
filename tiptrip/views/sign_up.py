import logging
from flet_route import Params, Basket
from flet import (
    Page, View, AppBar, Column, Container,
    Text, TextField, Checkbox, ElevatedButton, IconButton,
    MainAxisAlignment, TextAlign, padding, icons,
    ControlEvent
)

from data import db
from resources.config import *
from resources.functions import load_user_to_basket


logger = logging.getLogger(f"{PROJECT_NAME}.{__name__}")


class SignUpView:
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
            password=True,
            on_change=self.validate
        )
        self.chk_signup: Checkbox = Checkbox(
            label="Acepto Términos y Condiciones",
            value=False,
            on_change=self.validate
        )
        self.btn_submit: ElevatedButton = ElevatedButton(
            text="Crear usuario",
            width=COMPONENTS_WIDTH,
            disabled=True,
            on_click=self.submit
        )

    def view(self, page: Page, params: Params, basket: Basket) -> View:
        self.page = page
        self.params = params
        self.basket = basket

        return View(
            route="/sign_up",
            controls=[
                AppBar(
                    title=Text(value=""),
                    leading=IconButton(
                        icon=icons.ARROW_BACK,
                        on_click=self.go_back
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
                                    value="Crear cuenta",
                                    size=TITLE_SIZE
                                )
                            ),
                            Container(content=self.txt_username),
                            Container(content=self.txt_password),
                            Container(content=self.chk_signup),
                            Container(content=self.btn_submit)
                        ]
                    )
                )
            ]
        )

    def go_back(self, event: ControlEvent):
        self.page.banner.close_banner(event)
        if self.basket.get("role") == "admin":
            self.page.go(f"/home/{self.basket.get('username')}")
        else:
            self.page.go('/')

    def validate(self, event: ControlEvent) -> None:
        if all([
            self.txt_username.value,
            self.txt_password.value,
            self.chk_signup.value
        ]):
            self.btn_submit.disabled = False
        else:
            self.btn_submit.disabled = True
        self.page.update()

    def submit(self, event: ControlEvent) -> None:
        logger.info("Creando conexión a la base de datos...")
        connection = db.connect_to_db()

        logger.info("Verificando que el registro no exista...")
        conditions: dict = {
            "username": self.txt_username.value,
            "password": self.txt_password.value
        }
        record = db.get_record(connection, "users", conditions)

        if record is None:
            logger.info("Insertando nuevo registro...")
            values: list = [self.txt_username.value, self.txt_password.value]
            if self.basket.get("role") == "admin":
                values.append("admin")
            else:
                values.append("user")

            db.insert_record(connection, "users", values)
            conditions: dict = {"username": self.txt_username.value}
            record: list = db.get_record(connection, "users", conditions)
            load_user_to_basket(self.basket, record)

        logger.info(
            "Nuevo usuario con credenciales: {}|{} creado correctamente"
            .format(self.txt_username.value, self.txt_password.value)
        )

        logger.info("Cerrando conexión con la base de datos...")
        db.close_connection_to_db(connection)

        logger.info("Redirigiendo a la vista \"Inicio\" (\"/home\")...")
        self.page.go(f"/home/{self.txt_username.value}")
