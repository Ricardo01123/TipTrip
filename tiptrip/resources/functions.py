import flet as ft
from os import listdir
from os.path import join
from logging import Logger
from base64 import b64encode

from resources.config import *


# Navigation functions
def go_to_view(page: ft.Page, logger: Logger, route: str) -> None:
	logger.info(f"Redirecting to view \'{route}\'...")
	try:
		page.go(route)
	except Exception as e:
		logger.error(f"Error: {e}")
		page.go(route)


def encode_logfile() -> str:
	with open(join(TEMP_ABSPATH, f"{PROJECT_NAME}.log"), "rb") as file:
		return b64encode(file.read()).decode("utf-8")


# Places functions
def get_placecard_image(place_name: str) -> str:
	image_dir: str = format_place_name(place_name)

	path: str = join(ASSETS_ABSPATH, "places", image_dir)
	try:
		images: list = listdir(path)
		if images:
			return join("places", image_dir, images[0])
		else:
			return "default.png"

	except Exception:
		return "default.png"


def get_place_icon(classification: str) -> str:
	match classification.lower():
		case "arquitectura": return ft.Icons.LOCATION_CITY
		case "centro cultural": return ft.Icons.PEOPLE_ALT
		case "centro religioso": return ft.Icons.CHURCH
		case "escultura": return ft.Icons.HANDYMAN
		case "experiencia": return ft.Icons.TAG_FACES_ROUNDED
		case "monumento": return ft.Icons.BOOKMARK
		case "mural": return ft.Icons.PALETTE
		case "museo": return ft.Icons.MUSEUM_SHARP
		case "zona arqueológica": return ft.Icons.TEMPLE_HINDU
		case _: return ft.Icons.LOCATION_ON


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


def get_audio_id(type: str) -> int:
	files: list[str] = listdir(TEMP_ABSPATH)
	type_files: list[str] = [file for file in files if type in file]
	return len(type_files) + 1


# Geolocation functions
def is_location_permission_enabled(gl: ft.Geolocator, logger: Logger, data = None) -> bool:
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


# General functions
def get_user_image() -> str:
	files: list[str] = listdir(ASSETS_ABSPATH)
	for file in files:
		if file.startswith("user"):
			return file

	return "None"


def split_text(
		text: str,
		chunk_size: int = CHUNK_SIZE,
		chunk_overlay: int = CHUNK_OVERLAY,
		separator: str = CHUNK_SEPARATOR
	) -> list[str]:

    result: list = []
    start: int = 0
    while start < len(text):
        end: int = min(start + chunk_size, len(text))

        if separator in text[start:end]:
            end = text.rfind(separator, start, end) + 1
        elif end < len(text) and separator in text[end:end + chunk_overlay]:
            end = text.find(separator, end, end + chunk_overlay) + 1

        if end <= start:
            end = start + chunk_size

        # Añade el segmento y actualiza el inicio
        result.append(text[start:end].strip())
        start = end

    return result
