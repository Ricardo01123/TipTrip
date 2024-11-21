import flet as ft
from requests import get, Response
from logging import Logger, getLogger

from components.bars import *
from resources.config import *
from resources.functions import *
from components.place_card import PlaceCard
from resources.styles import txt_messages_style


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class FavoritesView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page

		# Custom components
		self.txt_favorite_searcher: ft.TextField = ft.TextField(
			prefix_icon=ft.icons.SEARCH,
			hint_text="Busca un sitio favorito",
			# on_change=self.search_favorite,
			**txt_messages_style
		)

		# # Places and pagination variables
		# self.items: list | ft.Container = self.get_favorites()

		# self.current_page: int = 0
		# self.items_per_page: int = 10
		# self.page_start_index: int = 0
		# self.page_end_index: int = self.items_per_page

		# self.lv_favorites_list: ft.ListView = ft.ListView(
		# 	padding=ft.padding.symmetric(
		# 		vertical=(SPACING / 2),
		# 		horizontal=SPACING
		# 	),
		# 	spacing=(SPACING / 2),
		# 	controls=(
		# 		self.items
		# 		if isinstance(self.items, ft.Container)
		# 		else self.items[self.page_start_index:self.page_end_index]
		# 	)
		# )

		# self.total_items: int = len(self.items)
		# self.total_pages: int = (self.total_items + self.items_per_page - 1) // self.items_per_page
		# self.lbl_actual_page: ft.Text = ft.Text(
		# 	value=f"Página {self.current_page + 1} de {self.total_pages}",
		# 	color=ft.colors.BLACK
		# )
		# self.cont_pagination: ft.Container = ft.Container(
		# 	width=self.page.width,
		# 	margin=ft.margin.only(bottom=5),
		# 	alignment=ft.alignment.center,
		# 	content=ft.Row(
		# 		controls=[
		# 			ft.Container(
		# 				margin=ft.margin.only(left=SPACING - 5),
		# 				content=ft.Icon(
		# 					name=ft.icons.ARROW_BACK_IOS_SHARP,
		# 					size=25,
		# 					color=ft.colors.BLACK
		# 				),
		# 				on_click=self.previous_page
		# 			),
		# 			ft.Container(
		# 				expand=True,
		# 				alignment=ft.alignment.center,
		# 				content=self.lbl_actual_page
		# 			),
		# 			ft.Container(
		# 				margin=ft.margin.only(right=SPACING - 5),
		# 				content=ft.Icon(
		# 					name=ft.icons.ARROW_FORWARD_IOS_SHARP,
		# 					size=25,
		# 					color=ft.colors.BLACK
		# 				),
		# 				on_click=self.next_page
		# 			),
		# 		]
		# 	)
		# )

		# View native attributes
		super().__init__(
			route="/favorites",
			bgcolor=ft.colors.WHITE,
			padding=ft.padding.all(value=0.0),
			spacing=0,
			controls=[
				TopBar(page=self.page, leading=True, logger=logger),
				ft.Container(
					width=self.page.width,
					height=RADIUS,
					bgcolor=MAIN_COLOR,
					border_radius=ft.border_radius.only(
						bottom_left=RADIUS,
						bottom_right=RADIUS
					),
					shadow=ft.BoxShadow(
						blur_radius=BLUR,
						color=ft.colors.GREY_800
					)
				),
				ft.Container(
					width=self.page.width,
					height=TXT_CONT_SIZE,
					margin=ft.margin.symmetric(vertical=10),
					content=ft.Row(
						controls=[
							ft.Container(expand=1),
							ft.Container(
								expand=8,
								bgcolor=ft.colors.WHITE,
								padding=ft.padding.symmetric(
									horizontal=(SPACING / 2)
								),
								border_radius=ft.border_radius.all(
									value=RADIUS
								),
								shadow=ft.BoxShadow(
									blur_radius=(BLUR / 2),
									offset=ft.Offset(0, 2),
									color=ft.colors.GREY
								),
								alignment=ft.alignment.center_left,
								content=self.txt_favorite_searcher
							),
							ft.Container(expand=1),
						]
					)
				),
				# self.cont_pagination,
				# ft.Container(
				# 	expand=True,
				# 	width=self.page.width,
				# 	content=self.lv_favorites_list
				# )
			],
			bottom_appbar=BottomBar(page=self.page, logger=logger, current_route="/favorites")
		)

	# def get_favorites(self) -> list | ft.Container:
	# 	logger.info("Calling Back-End API...")

	# 	response: Response = get(
	# 		url=f"{BACK_END_URL}/{FAVORITES_ENDPOINT}/{self.page.session.get('id')}",
	# 		headers={
	# 			"Content-Type": "application/json",
	# 			"Authorization": f"Bearer {self.page.session.get('session_token')}"
	# 		}
	# 	)

	# 	logger.info("Evaluating response...")
	# 	if response.status_code == 200:
	# 		favorites: dict = response.json()["favorites"]
	# 		logger.info(f"Obtained a total of {len(favorites)} favorite places...")
	# 		return [
	# 			PlaceCard(
	# 				page=self.page,
	# 				id=favorite["id"],
	# 				name=favorite["name"],
	# 				classification=favorite["classification"],
	# 				address=favorite["address"],
	# 				image_link=get_place_image(favorite["name"]),
	# 				is_favorite=True,
	# 				punctuation=favorite["punctuation"],
	# 			)
	# 			for favorite in favorites
	# 		]

	# 	elif response.status_code == 204:
	# 		return [
	# 			ft.Container(
	# 				alignment=ft.alignment.center,
	# 				content=ft.Text(
	# 					value="No se encontró ningún sitio turístico favorito.",
	# 					color=ft.colors.BLACK,
	# 					size=30
	# 				)
	# 			)
	# 		]

	# 	else:
	# 		return [
	# 			ft.Container(
	# 				alignment=ft.alignment.center,
	# 				content=ft.Text(
	# 					value=(
	# 						"Ocurrió un error al obtener la lista de sitios "
	# 						"turísticos favoritos.\nFavor de intentarlo de nuevo "
	# 						"más tarde."
	# 					),
	# 					color=ft.colors.BLACK,
	# 					size=30
	# 				)
	# 			)
	# 		]

	# def update_pagination_data(self, items: list) -> None:
	# 	self.current_page = 0
	# 	self.total_items = len(items)
	# 	self.total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
	# 	self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
	# 	self.page.update()

	# def search_favorite(self, _: ft.ControlEvent) -> None:
	# 	if self.txt_favorite_searcher.value == "":
	# 		logger.info("Cleaning 'searching favorite' filter...")
	# 		self.lv_favorites_list.controls = self.items[0:self.items_per_page]
	# 		self.update_pagination_data(self.items)
	# 	else:
	# 		value: str = self.txt_favorite_searcher.value.lower()
	# 		logger.info(f"Searching favorite... Searching for value {value}")
	# 		items: list = [
	# 			favorite for favorite in self.items if value in
	# 			# Searching in the structure of the PlaceCard component in place_card.py
	# 			favorite.content.controls[0].content.controls[0].value.lower()
	# 		]
	# 		self.lv_favorites_list.controls = items[0:self.items_per_page]
	# 		self.update_pagination_data(items)

	# def previous_page(self, _: ft.ControlEvent) -> None:
	# 	logger.info(f"Going to previous page...")
	# 	if self.current_page > 0:
	# 		self.current_page -= 1
	# 	else:
	# 		self.current_page = self.total_pages - 1

	# 	self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
	# 	self.set_page_indexes()
	# 	self.page.update()

	# def next_page(self, _: ft.ControlEvent) -> None:
	# 	logger.info(f"Going to next page...")
	# 	if self.current_page < self.total_pages - 1:
	# 		self.current_page += 1
	# 	else:
	# 		self.current_page = 0

	# 	self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
	# 	self.set_page_indexes()
	# 	self.page.update()
