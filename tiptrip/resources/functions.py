from flet import *
from time import sleep
from logging import Logger
from flet_route import Basket

from resources.config import (
	CDXM_MIN_LATITUDE, CDXM_MAX_LATITUDE, CDXM_MIN_LONGITUDE, CDXM_MAX_LONGITUDE
)


# Navigation functions
def go_to_view(page: Page, logger: Logger, route: str) -> None:
	logger.info(f"Redirecting to view \"/{route}\"...")
	page.go(f"/{route}")


# Basket functions
def clean_basket(basket: Basket, logger: Logger) -> None:
	logger.info("Cleaning session basket...")
	basket.delete("id")
	basket.delete("email")
	basket.delete("session_token")
	basket.delete("username")
	basket.delete("created_at")


# Places functions
def format_place_name(place_name: str) -> str:
	return place_name\
			.replace(' ', "_")\
			.replace('-', "_")\
			.replace(',', "")\
			.replace('.', "")\
			.replace(':', "")\
			.replace(';', "")\
			.replace('(', "")\
			.replace(')', "")\
			.replace('Á', 'A')\
			.replace('É', 'E')\
			.replace('Í', 'I')\
			.replace('Ó', 'O')\
			.replace('Ú', 'U')\
			.replace('á', 'a')\
			.replace('é', 'e')\
			.replace('í', 'i')\
			.replace('ó', 'o')\
			.replace('ú', 'u')\
			# .replace('Ñ', 'N')\
			# .replace('ñ', 'n')


# Geolocation functions
def is_location_permission_enabled(gl: Geolocator,logger: Logger) -> bool:

	try:
		status: GeolocatorPermissionStatus = gl.get_permission_status()
		logger.info(f"Location permission status: {status}")
		if status in [
			GeolocatorPermissionStatus.ALWAYS,
			GeolocatorPermissionStatus.WHILE_IN_USE
		]:
			return True
		return False

	except Exception as e:
		logger.error(f"Error getting location permission status: {e}")
		return False


def request_location_permissions(gl: Geolocator, logger: Logger) -> bool:
	try:
		logger.info("Opening device's location settings...")
		gl.request_permission(wait_timeout=60)
		# gl.open_location_settings()
		sleep(5)

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
