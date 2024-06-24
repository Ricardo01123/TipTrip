from typing import Any
from flet import margin, padding, border_radius, BoxShadow, InputBorder, colors

from resources.config import *


cont_main_style: dict[str, Any] = {
	"expand": True,
	"width": (APP_WIDTH - (SPACING * 2)),
	"bgcolor": colors.WHITE,
	"margin": margin.all(value=SPACING),
	"padding": padding.all(value=SPACING),
	"border_radius": border_radius.all(value=RADIUS),
	"shadow": BoxShadow(blur_radius=LOW_BLUR),
}


txt_style: dict[str, Any] = {
	"height": 40,
	"label": None,
	"text_size": 18,
	"cursor_color": SECONDARY_COLOR,
	"focused_border_color": SECONDARY_COLOR,
	"border": InputBorder.UNDERLINE
}


txt_messages_style: dict[str, Any] = {

}


btn_primary_style: dict[str, Any] = {
	"color": colors.WHITE,
	"bgcolor": MAIN_COLOR,
	"width": (APP_WIDTH - (SPACING * 4)),
	"disabled": True
}


btn_secondary_style: dict[str, Any] = {
	"color": MAIN_COLOR,
	"width": (APP_WIDTH - (SPACING * 4))
}

btn_danger_style: dict[str, Any] = {
	"color": colors.RED,
	"width": (APP_WIDTH - (SPACING * 4))
}