from flet import *
from typing import Any

from resources.config import *


cont_main_style: dict[str, Any] = {
	"expand": True,
	"bgcolor": colors.WHITE,
	"margin": margin.all(value=SPACING),
	"padding": padding.all(value=SPACING),
	"border_radius": border_radius.all(value=RADIUS),
	"shadow": BoxShadow(blur_radius=LOW_BLUR),
}


txt_style: dict[str, Any] = {
	"height": 45,
	"label": None,
	"text_size": 19,
	"color": colors.BLACK,
	"hint_style": TextStyle(color=colors.GREY_600),
	"cursor_color": SECONDARY_COLOR,
	"focused_border_color": SECONDARY_COLOR,
	"border": InputBorder.UNDERLINE
}


txt_messages_style: dict[str, Any] = {
	"height": 45,
	"label": None,
	"text_size": 19,
	"color": colors.BLACK,
	"hint_style": TextStyle(color=colors.GREY_600),
	"cursor_color": SECONDARY_COLOR,
	"focused_border_color": SECONDARY_COLOR,
	"border": InputBorder.NONE
}


btn_primary_style: dict[str, Any] = {
	"color": colors.WHITE,
	"bgcolor": SECONDARY_COLOR,
	"height": BTN_HEIGHT,
	"elevation": BTN_ELEVATION
}


btn_secondary_style: dict[str, Any] = {
	"color": SECONDARY_COLOR,
	"bgcolor": colors.WHITE,
	"height": BTN_HEIGHT,
	"elevation": BTN_ELEVATION
}


btn_danger_style: dict[str, Any] = {
	"color": colors.RED,
	"bgcolor": colors.WHITE,
	"height": BTN_HEIGHT,
	"elevation": BTN_ELEVATION
}
