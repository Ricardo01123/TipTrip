from flet import (
    Page, View, AppBar, Column, Container,
    Text, TextField, ElevatedButton,
    MainAxisAlignment, TextAlign, padding,
    ControlEvent
)

from data.db import *
from resources.config import *


def forgotten_pwd_view(page: Page) -> View:
    txt_username: TextField = TextField(
                                    label="Nombre de usuario",
                                    text_align=TextAlign.LEFT,
                                    width=COMPONENTS_WIDTH
                                )
    txt_password: TextField = TextField(
                                    label="Contraseña",
                                    text_align=TextAlign.LEFT,
                                    width=COMPONENTS_WIDTH,
                                    disabled=True
                                )
    btn_submit: ElevatedButton = ElevatedButton(
                                        text="Recuperar contraseña",
                                        width=COMPONENTS_WIDTH,
                                        disabled=True
                                    )

    def validate(event: ControlEvent) -> None:
        btn_submit.disabled = False if txt_username.value else True
        page.update()

    def submit(event: ControlEvent) -> None:
        connection = connect_to_db()
        if check_record_exists(connection, txt_username.value):
            password = get_password(connection, txt_username.value)
            txt_password.value = password
            txt_password.disabled = False
            btn_submit.disabled = True
            print(
                "Contraseña de usuario: "
                f"{txt_username.value} recuperada con éxito"
            )
            page.update()

    txt_username.on_change = validate
    btn_submit.on_click = submit

    return View(
        route="/forgotten_pwd",
        controls=[
            AppBar(
                title=Text(value=""),
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
                                size=30
                            )
                        ),
                        Container(
                            content=Text(
                                value="Recuperar contraseña",
                                size=15
                            )
                        ),
                        Container(content=txt_username),
                        Container(content=txt_password),
                        Container(content=btn_submit)
                    ]
                )
            )
        ]
    )
