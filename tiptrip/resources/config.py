from os import getcwd
from os.path import join
from pyaudio import paInt16


# Names
PROJECT_NAME: str = "TIP TRIP"
BOT_NAME: str = "Bot"

# Text sizes
PROJECT_NAME_SIZE: int = 40
PAGE_SUBTITLE_SIZE: int = 20
BTN_TEXT_SIZE: int = 15

PLC_TITLE_SIZE: int = 22
PLC_CATEGORY_SIZE: int = 16
MESSAGE_TEXT_SIZE: int = 18

# Colors
MAIN_COLOR: str = "#FF7F11"  # orange
SECONDARY_COLOR: str = "#006E7E"  # blue

# Components variables
SPACING: int = 25
RADIUS: int = 20
BLUR: int = 10
LOW_BLUR: int = 7

TXT_CONT_SIZE: int = 50
CONT_MESSAGE_HEIGHT: int = 80
BTN_HEIGHT: int = 50
BTN_ELEVATION: int = 5

PROFILE_IMAGE_DIMENSIONS: int = 200
PLACE_DETAILS_IMAGE_WIDTH: int = 300
PLACE_DETAILS_IMAGE_HEIGHT: int = 270
PLACE_DETAILS_CONT_TITLE_HEIGHT: int = 80

LOADING_RING_SIZE: int = 50

# Other variables
LOGGING_FORMAT: str = "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
RGX_EMAIL: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Back-End API
BACK_END_URL: str = "http://145.223.74.225:5000"
# BACK_END_URL: str = "http://127.0.0.1:5000"
PLACES_ENDPOINT: str = "places"
USERS_ENDPOINT: str = "users"
AUTH_USER_ENDPOINT: str = "users/auth"
FAVORITES_ENDPOINT: str = "users/favorites"
AGENT_ENDPOINT: str = "models/agent"
ASR_ENDPOINT: str = "models/asr"

# Chatbot audio file
FORMAT: int = paInt16
CHANNELS: int = 1
CHUNK: int = 1_024
SAMPLING_RATE: int = 16_000
TEMP_FILE_NAME: str = "temp_audio.wav"
RECEIVED_TEMP_FILE_NAME: str = "received_temp_audio.wav"

# Geolocation variables
CDXM_MIN_LATITUDE: float = 19 + 3 / 60
CDXM_MAX_LATITUDE: float = 19 + 36 / 60
CDXM_MIN_LONGITUDE: float = -99 - 22 / 6
CDXM_MAX_LONGITUDE: float = -98 - 57 / 60

# Project paths
PROJECT_DIR_ABSPATH: str = getcwd()
TEMP_ABSPATH: str = join(PROJECT_DIR_ABSPATH, "temp")
ASSETS_ABSPATH: str = join(PROJECT_DIR_ABSPATH, "assets")

# Places filters variables
MUNICIPALITIES: list[str] = [
	"Álvaro Obregón",
	"Azcapotzalco",
	"Benito Juárez",
	"Coyoacán",
	"Cuajimalpa de Morelos",
	"Cuauhtémoc",
	"Gustavo A. Madero",
	"Iztacalco",
	"Iztapalapa",
	"La Magdalena Contreras",
	"Miguel Hidalgo",
	"Milpa Alta",
	"San Ángel",
	"Tláhuac",
	"Tlalpan",
	"Venustiano Carranza",
	"Xochimilco"
]

CLASSIFICATIONS: list[str] = [
	"Arquitectura",
	"Centro cultural",
	"Centro religioso",
	"Escultura",
	"Experiencia",
	"Monumento",
	"Mural",
	"Museo",
	"Zona arqueológica"
]
