import flet as ft
from os import listdir
from logging import Logger
from os.path import join, exists

from resources.config import *


# Navigation functions
def go_to_view(page: ft.Page, logger: Logger, route: str) -> None:
	logger.info(f"Redirecting to view \'{route}\'...")
	page.go(route)


# Places functions
def get_place_image(place_name: str) -> str:
	dir: str = format_place_name(place_name)

	path: str = join(ASSETS_ABSPATH, "places", dir)
	if exists(path):
		images: list = listdir(path)
		if images:
			return join("places", dir, images[0])
		else:
			return ["/default.png"]
	else:
		return ["/default.png"]


def get_place_icon(classification: str) -> str:
	match classification.lower():
		case "arquitectura": return ft.icons.LOCATION_CITY
		case "centro cultural": return ft.icons.PEOPLE_ALT
		case "centro religioso": return ft.icons.CHURCH
		case "escultura": return ft.icons.HANDYMAN
		case "experiencia": return ft.icons.TAG_FACES_ROUNDED
		case "monumento": return ft.icons.BOOKMARK
		case "mural": return ft.icons.PALETTE
		case "museo": return ft.icons.MUSEUM_SHARP
		case "zona arqueológica": return ft.icons.TEMPLE_HINDU
		case _: return ft.icons.LOCATION_ON


def format_place_name(place_name: str) -> str:
	return place_name\
		.replace(' ', "_")\
		.replace('-', "_")\
		.replace("'", "")\
		.replace(',', "")\
		.replace('.', "")\
		.replace(':', "")\
		.replace(';', "")\
		.replace('(', "")\
		.replace(')', "")\
		.replace('Á', 'A')\
		.replace('É', 'E')\
		.replace('Í', 'I')\
		.replace('Ñ', 'N')\
		.replace('Ó', 'O')\
		.replace('Ú', 'U')\
		.replace('á', 'a')\
		.replace('é', 'e')\
		.replace('í', 'i')\
		.replace('ó', 'o')\
		.replace('ú', 'u')\
		.replace('ñ', 'n')


# Geolocation functions
def is_location_permission_enabled(gl: ft.Geolocator, logger: Logger) -> bool:
	try:
		status: ft.GeolocatorPermissionStatus = gl.get_permission_status()
		logger.info(f"Location permission status: {status}")
		if status in [
			ft.GeolocatorPermissionStatus.ALWAYS,
			ft.GeolocatorPermissionStatus.WHILE_IN_USE
		]:
			return True
		return False

	except Exception as e:
		logger.error(f"Error getting location permission status: {e}")
		return False


def request_location_permissions(gl: ft.Geolocator, logger: Logger) -> bool:
	try:
		logger.info("Opening device's location settings...")
		gl.request_permission(wait_timeout=60)

		logger.info("Validating location permissions...")
		if is_location_permission_enabled(gl, logger):
			return True
		return False

	except Exception as e:
		logger.error(f"Error requesting location permissions: {e}")
		return False


def is_inside_cdmx(current_position: tuple[float, float]) -> bool:
	if CDXM_MIN_LATITUDE <= current_position[0] <= CDXM_MAX_LATITUDE and \
		CDXM_MIN_LONGITUDE <= current_position[1] <= CDXM_MAX_LONGITUDE:
		return True
	return False
