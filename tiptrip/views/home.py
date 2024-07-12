from requests import get, Response
from requests.auth import HTTPBasicAuth

from logging import getLogger
from flet_route import Params, Basket

from flet import (
	Page, View, Container, ListView, Column, Row, Text, TextField, CircleAvatar,
	Icon, AlertDialog, MainAxisAlignment, Offset, alignment, padding, margin,
	BoxShadow, border_radius, colors, icons,
)

from components.bars import *
from resources.config import *
from resources.functions import *
from components.place_card import PlaceCard
from resources.styles import txt_messages_style


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class HomeView:
	def __init__(self) -> None:
		self.page = None
		self.params = None
		self.basket = None

		self.route = "/home"
		self.lv_places_list = None
		self.dlg_categories = None

		self.txt_place: TextField = TextField(
			prefix_icon=icons.SEARCH,
			hint_text="Busca un lugar",
			**txt_messages_style
			# on_change=self.validate
		)

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.lv_places_list: ListView = ListView(
			padding=padding.symmetric(
				vertical=(SPACING / 2),
				horizontal=SPACING
			),
			spacing=(SPACING / 2),
			controls=self.get_places()
		)

		# self.dlg_categories: AlertDialog = AlertDialog(
		# 	modal=True,
		# 	title=Text("Filtrar lugares"),
		# 	content=Column(
		# 		spacing=(SPACING / 2),
		# 		controls=[
		# 			Text(value="Monumento"),
		# 			Text(value="Arquitectura"),
		# 			Text(value="Centro Cultural"),
		# 			Text(value="Catedral/Templo"),
		# 			Text(value="Museo"),
		# 			Text(value="Zona arqueológica"),
		# 			Text(value="Plaza"),
		# 			Text(value="Experiencia")
		# 		]
		# 	),
		# 	actions=[
		# 		TextButton(
		# 			text="Aceptar",
		# 			on_click=HomeView.close_dialog
		# 		)
		# 	]
		# )

		# self.page.dialog = self.dlg_categories

		return View(
			route=self.route,
			bgcolor=colors.WHITE,
			padding=padding.all(value=0.0),
			spacing=0,
			controls=[
				TopBar(page=self.page, leading=False, logger=logger),
				Container(
					width=self.page.width,
					height=RADIUS,
					bgcolor=MAIN_COLOR,
					border_radius=border_radius.only(
						bottom_left=RADIUS,
						bottom_right=RADIUS
					),
					shadow=BoxShadow(
						blur_radius=BLUR,
						color=colors.GREY_800
					),
				),
				Container(
					width=self.page.width,
					height=TXT_CONT_SIZE,
					margin=margin.symmetric(vertical=10),
					content=Row(
						controls=[
							Container(expand=1),
							Container(
								expand=8,
								bgcolor=colors.WHITE,
								padding=padding.symmetric(
									horizontal=(SPACING / 2)
								),
								border_radius=border_radius.all(
									value=RADIUS
								),
								shadow=BoxShadow(
									blur_radius=(BLUR / 2),
									offset=Offset(0, 2),
									color=colors.GREY
								),
								content=Row(
									alignment=MainAxisAlignment.SPACE_BETWEEN,
									spacing=None,
									controls=[
										Container(
											expand=4,
											content=self.txt_place,
										),
										Container(
											expand=1,
											content=CircleAvatar(
												bgcolor=colors.WHITE,
												radius=SPACING,
												content=Icon(
													name=icons.FILTER_LIST,
													color=colors.BLACK
												)
											),
											# on_click=self.open_dialog
										)
									]
								)
							),
							Container(expand=1),
						]
					)
				),
				Container(
					expand=True,
					width=self.page.width,
					content=self.lv_places_list
				),
				BottomBar(
					page=self.page,
					logger=logger,
					current_route=self.route
				)
			]
		)

	# def open_dialog(self, event: ControlEvent) -> None:
	# 	self.dlg_categories.open = True
	# 	self.page.update()

	# def close_dialog(self, event: ControlEvent) -> None:
	# 	self.dlg_categories.open = False
	# 	self.page.update()

	def get_places(self) -> list:
		response: Response = get(
			f"{BACK_END_URL}{GET_ALL_RECORDS_ENDPOINT}",
			json={"table_name": "sitios_turisticos"},
			headers=REQUEST_HEADERS,
			auth=HTTPBasicAuth("admin", "admin")
		)

		if response.status_code != 200:
			return [
				Container(
					alignment=alignment.center,
					content=Text(
						value="No se encontró ningún lugar.",
						color=colors.BLACK,
						size=35
					)
				)
			]
		else:
			places_data: dict = response.json()["data"]
			return [
				PlaceCard(
					page=self.page,
					title=place["nombre"],
					category=place["clasificacion_sitio"],
					punctuation=place["puntuacion"],
					image_link=place["ruta"],
					address=(
						f"{place['calle_numero']}, "
						f"{place['colonia']}, "
						f"{place['cp']}, "
						f"{place['delegacion_municipio']}, "
						f"{place['entidad_federativa']}."
					)
				)
				for place in places_data
			]
