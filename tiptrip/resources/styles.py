import flet as ft
from typing import Any

from resources.config import *


cont_main_style: dict[str, Any] = {
	"expand": True,
	"bgcolor": ft.Colors.WHITE,
	"margin": ft.margin.all(value=SPACING),
	"padding": ft.padding.all(value=SPACING),
	"border_radius": ft.border_radius.all(value=RADIUS),
	"shadow": ft.BoxShadow(blur_radius=LOW_BLUR),
}


txt_style: dict[str, Any] = {
	"height": 45,
	"label": None,
	"text_size": 19,
	"color": ft.Colors.BLACK,
	"hint_style": ft.TextStyle(color=ft.Colors.GREY_600),
	"cursor_color": SECONDARY_COLOR,
	"focused_border_color": SECONDARY_COLOR,
	"border": ft.InputBorder.UNDERLINE
}


txt_messages_style: dict[str, Any] = {
	"height": 45,
	"label": None,
	"text_size": 19,
	"color": ft.Colors.BLACK,
	"hint_style": ft.TextStyle(color=ft.Colors.GREY_600),
	"cursor_color": SECONDARY_COLOR,
	"focused_border_color": SECONDARY_COLOR,
	"border": ft.InputBorder.NONE
}


btn_primary_style: dict[str, Any] = {
	"color": ft.Colors.WHITE,
	"bgcolor": SECONDARY_COLOR,
	"height": BTN_HEIGHT,
	"elevation": BTN_ELEVATION
}


btn_secondary_style: dict[str, Any] = {
	"color": SECONDARY_COLOR,
	"bgcolor": ft.Colors.WHITE,
	"height": BTN_HEIGHT,
	"elevation": BTN_ELEVATION
}


btn_danger_style: dict[str, Any] = {
	"color": ft.Colors.RED,
	"bgcolor": ft.Colors.WHITE,
	"height": BTN_HEIGHT,
	"elevation": BTN_ELEVATION
}
