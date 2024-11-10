from flet import *
from os import listdir
from os.path import join
from logging import getLogger
from requests import get, Response
from flet_route import Params, Basket

from components.bars import *
from resources.config import *
from resources.functions import *
from components.place_card import PlaceCard
from resources.styles import txt_messages_style


logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class FavoritesView:
	def __init__(self) -> None:
		self.route = "/favorites"

	def view(self, page: Page, params: Params, basket: Basket) -> View:
		self.page = page
		self.params = params
		self.basket = basket

		self.txt_favorite_searcher: TextField = TextField(
			prefix_icon=icons.SEARCH,
			hint_text="Busca un sitio favorito",
			on_change=self.search_favorite,
			**txt_messages_style
		)

		# Places and pagination variables
		self.items: list | Container = self.get_favorites()

		self.current_page: int = 0
		self.items_per_page: int = 10
		self.page_start_index: int = 0
		self.page_end_index: int = self.items_per_page

		self.lv_favorites_list: ListView = ListView(
			padding=padding.symmetric(
				vertical=(SPACING / 2),
				horizontal=SPACING
			),
			spacing=(SPACING / 2),
			controls=(
				self.items
				if isinstance(self.items, Container)
				else self.items[self.page_start_index:self.page_end_index]
			)
		)

		self.total_items: int = len(self.items)
		self.total_pages: int = (self.total_items + self.items_per_page - 1) // self.items_per_page
		self.lbl_actual_page: Text = Text(
			value=f"Página {self.current_page + 1} de {self.total_pages}",
			color=colors.BLACK
		)
		self.cont_pagination: Container = Container(
			width=self.page.width,
			margin=margin.only(bottom=5),
			alignment=alignment.center,
			content=Row(
				controls=[
					Container(
						margin=margin.only(left=SPACING - 5),
						content=Icon(
							name=icons.ARROW_BACK_IOS_SHARP,
							size=25,
							color=colors.BLACK
						),
						on_click=self.previous_page
					),
					Container(
						expand=True,
						alignment=alignment.center,
						content=self.lbl_actual_page
					),
					Container(
						margin=margin.only(right=SPACING - 5),
						content=Icon(
							name=icons.ARROW_FORWARD_IOS_SHARP,
							size=25,
							color=colors.BLACK
						),
						on_click=self.next_page
					),
				]
			)
		)

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
					)
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
								alignment=alignment.center_left,
								content=self.txt_favorite_searcher
							),
							Container(expand=1),
						]
					)
				),
				self.cont_pagination,
				Container(
					expand=True,
					width=self.page.width,
					content=self.lv_favorites_list
				),
				BottomBar(
					page=self.page,
					logger=logger,
					current_route=self.route
				)
			]
		)


	def get_favorites(self) -> list | Container:
		logger.info("Calling Back-End API...")

		response: Response = get(
			url=f"{BACK_END_URL}/{FAVORITES_ENDPOINT}/{self.basket.get('id')}",
			headers={
				"Content-Type": "application/json",
				"Authorization": f"Bearer {self.basket.get('session_token')}"
			}
		)

		logger.info("Evaluating response...")
		if response.status_code == 200:
			favorites: dict = response.json()["favorites"]
			logger.info(f"Obtained a total of {len(favorites)} favorite places...")
			return [
				PlaceCard(
					page=self.page,
					basket=self.basket,
					id=favorite["id"],
					name=favorite["name"],
					classification=favorite["classification"],
					address=favorite["address"],
					image_link=get_place_image(favorite["name"]),
					is_favorite=True,
					punctuation=favorite["punctuation"],
				)
				for favorite in favorites
			]

		elif response.status_code == 204:
			return [
				Container(
					alignment=alignment.center,
					content=Text(
						value="No se encontró ningún sitio turístico favorito.",
						color=colors.BLACK,
						size=30
					)
				)
			]

		else:
			return [
				Container(
					alignment=alignment.center,
					content=Text(
						value=(
							"Ocurrió un error al obtener la lista de sitios "
							"turísticos favoritos.\nFavor de intentarlo de nuevo "
							"más tarde."
						),
						color=colors.BLACK,
						size=30
					)
				)
			]

	def update_pagination_data(self, items: list) -> None:
		self.current_page = 0
		self.total_items = len(items)
		self.total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
		self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
		self.page.update()

	def search_favorite(self, _: ControlEvent) -> None:
		if self.txt_favorite_searcher.value == "":
			logger.info("Cleaning 'searching favorite' filter...")
			self.lv_favorites_list.controls = self.items[0:self.items_per_page]
			self.update_pagination_data(self.items)
		else:
			value: str = self.txt_favorite_searcher.value.lower()
			logger.info(f"Searching favorite... Searching for value {value}")
			items: list = [
				favorite for favorite in self.items if value in
				# Searching in the structure of the PlaceCard component in place_card.py
				favorite.content.controls[0].content.controls[0].value.lower()
			]
			self.lv_favorites_list.controls = items[0:self.items_per_page]
			self.update_pagination_data(items)

	def previous_page(self, _: ControlEvent) -> None:
		logger.info(f"Going to previous page...")
		if self.current_page > 0:
			self.current_page -= 1
		else:
			self.current_page = self.total_pages - 1

		self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
		self.set_page_indexes()
		self.page.update()

	def next_page(self, _: ControlEvent) -> None:
		logger.info(f"Going to next page...")
		if self.current_page < self.total_pages - 1:
			self.current_page += 1
		else:
			self.current_page = 0

		self.lbl_actual_page.value = f"Página {self.current_page + 1} de {self.total_pages}"
		self.set_page_indexes()
		self.page.update()
