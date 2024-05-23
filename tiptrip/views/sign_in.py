from flet import (
    Page, View, Column, Row, Container,
    Text, TextField, TextButton, ElevatedButton,
    MainAxisAlignment, TextAlign, padding,
    ControlEvent
)

from data.db import *
from resources.config import *


def sign_in_view(page: Page) -> View:
    txt_username: TextField = TextField(
                                    label="Nombre de usuario",
                                    text_align=TextAlign.LEFT,
                                    width=COMPONENTS_WIDTH
                                )
    txt_password: TextField = TextField(
                                    label="Contraseña",
                                    text_align=TextAlign.LEFT,
                                    width=COMPONENTS_WIDTH,
                                    password=True
                                )
    btn_submit: ElevatedButton = ElevatedButton(
                                        text="Iniciar sesión",
                                        width=COMPONENTS_WIDTH,
                                        disabled=True
                                    )

    def validate(event: ControlEvent) -> None:
        if all([txt_username.value, txt_password.value]):
            btn_submit.disabled = False
        else:
            btn_submit.disabled = True
        page.update()

    def submit(event: ControlEvent) -> None:
        connection = connect_to_db()
        data = (txt_username.value, txt_password.value)

        if check_record_exists(connection, data):
            print(
                "Usuario con credenciales:\n"
                f"    Nombre de usuario: {data[0]}\n"
                f"    Contraseña: {data[1]}\n"
                "inició sesión con éxito"
            )
            close_connection_to_db(connection)

            page.go("/home")

    txt_username.on_change = validate
    txt_password.on_change = validate
    btn_submit.on_click = submit

    return View(
        route='/',
        controls=[
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
                                size=30
                            )
                        ),
                        Container(
                            content=Text(
                                value="Iniciar sesión",
                                size=15
                            )
                        ),
                        Container(content=txt_username),
                        Container(content=txt_password),
                        Container(content=btn_submit),
                        Row(
                            width=COMPONENTS_WIDTH,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                Container(
                                    TextButton(
                                        text="Crear cuenta",
                                        on_click=lambda _: page.go("/sign_up")
                                    )
                                ),
                                Container(
                                    TextButton(
                                        text="Olvidé mi contraseña",
                                        on_click=lambda _:
                                            page.go("/forgotten_pwd")
                                    ),
                                )
                            ]
                        )
                    ]
                )
            )
        ]
    )
