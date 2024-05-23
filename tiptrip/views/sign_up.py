from flet import (
    Page, View, AppBar, Column, Container,
    Text, TextField, Checkbox, ElevatedButton,
    MainAxisAlignment, TextAlign, padding,
    ControlEvent
)

from data.db import *
from resources.config import *


def sign_up_view(page: Page) -> View:
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
    chk_signup: Checkbox = Checkbox(
                                label="Acepto términos y condiciones",
                                value=False
                            )
    btn_submit: ElevatedButton = ElevatedButton(
                                        text="Crear usuario",
                                        width=COMPONENTS_WIDTH,
                                        disabled=True
                                    )

    def validate(event: ControlEvent) -> None:
        if all([txt_username.value, txt_password.value, chk_signup.value]):
            btn_submit.disabled = False
        else:
            btn_submit.disabled = True
        page.update()

    def submit(event: ControlEvent) -> None:
        connection = connect_to_db()
        data = (txt_username.value, txt_password.value)

        if not check_record_exists(connection, data):
            insert_record(connection, data)

        new_user = get_all_records(connection)[-1]
        print(
            "Usuario con credenciales:\n"
            f"    Nombre de usuario: {new_user[0]}\n"
            f"    Contraseña: {new_user[1]}\n"
            "creado con éxito"
        )
        close_connection_to_db(connection)

        page.go("/home")

    txt_username.on_change = validate
    txt_password.on_change = validate
    chk_signup.on_change = validate
    btn_submit.on_click = submit

    return View(
        route="/sign_up",
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
                                value="Crear cuenta",
                                size=15
                            )
                        ),
                        Container(content=txt_username),
                        Container(content=txt_password),
                        Container(content=chk_signup),
                        Container(content=btn_submit)
                    ]
                )
            )
        ]
    )
