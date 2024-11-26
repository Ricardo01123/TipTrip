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
# BACK_END_URL: str = "http://145.223.74.225:5000"
BACK_END_URL: str = "http://127.0.0.1:5000"
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

LOCATION_PHRASES: list[str] = [
    "cercano", "cerca de mi", "cerca de mi ubicacion", "cerca de donde estoy", "cerca de aqui", "cerca de mi posicion",
    "alrededor", "en mi area", "alrededor de mi", "en mi ubicacion", "desde mi ubicacion",
    "en mi posicion actual", "alrededor de donde estoy", "alrededor de mi ubicacion",
    "en las cercanias", "cerca de mi zona", "en mi zona", "cerca de este lugar", "cerca de este sitio",
    "alrededor de este sitio", "en los alrededores", "cerca de mi direccion", "en esta area", "en esta ubicacion",
    "en mi proximidad", "en mi entorno", "en esta zona", "cerca de mi lugar actual", "cerca de donde me encuentro",
    "en el area de mi ubicacion", "cerca del punto donde estoy", "en mi vecindad", "por aqui",
    "en los alrededores de aqui", "en los alrededores de mi posicion", "en esta proximidad", "en las inmediaciones",
    "en mi posicion geografica", "donde me encuentro ahora", "en mi ubicacion actual", "cerca de mi lugar",
    "cerca de la ubicacion actual", "en mi posicion geolocalizada", "en las cercanias de aqui",
    "en el area alrededor de mi", "donde estoy ahora", "cerca del lugar donde estoy", "por mi area",
    "en este lugar", "por mi ubicacion", "en el sitio donde estoy", "en este mismo lugar", "por los alrededores",
    "en esta area geografica", "cerca de mi posicion exacta", "en el entorno donde estoy", "en mi lugar actual",
    "alrededor de este punto", "donde me encuentro en este momento", "en esta zona especifica",
    "cerca de aqui mismo", "cerca de esta ubicacion exacta", "en las proximidades de aqui", "alrededor de donde me ubico",
    "en el area cercana a mi", "en los alrededores de mi sitio", "alrededor de esta area",
    "cerca del lugar donde me encuentro", "en mi ubicacion de ahora", "alrededor de mi punto actual",
    "en el lugar donde me ubico", "cerca de este punto exacto", "en las cercanias donde estoy",
    "alrededor de esta posicion", "dentro de mi radio", "en la vecindad de aqui", "en los alrededores inmediatos",
    "por donde estoy ahora", "cerca de este lugar preciso", "en las cercanias de esta posicion",
    "cerca del sitio donde estoy", "en mi ubicacion especifica", "por los alrededores donde me ubico",
    "en este punto exacto", "en la zona donde me encuentro", "en la proximidad donde estoy", "por la ubicacion actual",
    "en el sitio exacto donde estoy"
]
