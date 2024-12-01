from os import getcwd
from os.path import join


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
SPACING: int = 15
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
PLACES_ENDPOINT: str = "places"
USERS_ENDPOINT: str = "users"
AUTH_USER_ENDPOINT: str = "users/auth"
FAVORITES_ENDPOINT: str = "users/favorites"
AGENT_ENDPOINT: str = "models/agent"
ASR_ENDPOINT: str = "models/asr"

# Chatbot audio file
CHANNELS: int = 1
CHUNK: int = 1_024
SAMPLING_RATE: int = 16_000
TEMP_USER_AUDIO_FILENAME: str = "temp_user_audio.wav"
TEMP_AGENT_AUDIO_FILENAME: str = "temp_agent_audio.wav"

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
	"Seleccionar todas",
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
	"Seleccionar todas",
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
	"cercano", "cerca de mi", "cerca de mí", "cerca de mi ubicacion", "cerca de mí ubicación", "cerca de mi ubicación", "cerca de mí ubicacion"
	"cerca de donde estoy", "cerca de dónde estoy", "cerca de aquí", "cerca de aqui", "cerca de mi posicion", "cerca de mí posición", "cerca de mí posicion", "cerca de mi posición",
	"alrededor", "en mi area", "en mi área", "por mi area", "por mi área", "alrededor de mi", "alrededor de mí",
	"en mi ubicacion", "en mi ubicación", "en mí ubicacion", "en mí ubicación", "desde mi ubicacion", "desde mi ubicación", "desde mí ubicacion", "desde mí ubicación",
	"en mi posicion actual", "en mi posición actual", "en mí posicion actual", "en mí posición actual", "alrededor de donde estoy", "alrededor de dónde estoy",
	"alrededor de mi ubicacion", "alrededor de mí ubicación", "alrededor de mí ubicacion", "alrededor de mi ubicación", "en las cercanias", "en las cercanías",
	"por las cercanias", "por las cercanías", "cerca de mi zona", "cerca de mí zona", "en mi zona", "en mí zona", "cerca de este lugar", "cerca de éste lugar", "cerca de este sitio", "cerca de éste lugar", "cerca de éste sitio",
	"por mi zona", "por mí zona", "alrededor de éste sitio", "alrededor de este sitio", "en los alrededores", "cerca de mi direccion", "cerca de mí dirección", "cerca de mí direccion", "cerca de mi dirección",
	"en esta area", "en esta área", "por esta area", "por esta área", "en esta ubicacion", "en esta ubicación", "en ésta ubicacion", "en ésta ubicación",
	"en mi proximidad", "en mí proximidad", "en mi entorno", "en mí entorno", "en esta zona", "en ésta zona", "por esta zona", "por ésta zona", "cerca de mi lugar actual",
	"cerca de mí lugar actual", "cerca de donde me encuentro", "cerca de dónde me encuentro",
	"en el area de mi ubicacion", "en el area de mi ubicación", "en el area de mí ubicacion",
	"en el area de mí ubicación", "en el área de mi ubicacion", "en el área de mi ubicación",
	"en el área de mí ubicacion", "en el área de mí ubicación",
	"cerca del punto donde estoy", "cerca del punto dónde estoy",
	"en mi vecindad", "en mí vecindad", "por aqui", "por aquí", "en los alrededores de aqui", "en los alrededores de aquí",
	"en los alrededores de mi posicion", "en los alrededores de mí posición",
	"en los alrededores de mí posicion", "en los alrededores de mi posición",
	"en esta proximidad", "en las inmediaciones",
	"en mi posicion geografica", "en mi posicion geográfica", "en mi posición geografica",
	"en mi posición geográfica", "en mí posicion geografica", "en mí posicion geográfica",
	"en mí posición geografica", "en mí posición geográfica",
	"donde me encuentro ahora", "dónde me encuentro ahora",
	"en mi ubicacion actual", "en mí ubicación actual", "en mí ubicacion actual", "en mi ubicación actual",
	"cerca de mi lugar", "cerca de mí lugar", "cerca de la ubicacion actual", "cerca de la ubicación actual",
	"en mi posicion geolocalizada", "en mí posición geolocalizada", "en mí posicion geolocalizada", "en mi posición geolocalizada",
	"en las cercanias de aqui", "en las cercanías de aquí", "en las cercanías de aqui", "en las cercanias de aquí",
	"en el area alrededor de mi", "en el área alrededor de mí", "en el área alrededor de mi", "en el area alrededor de mi",
	"donde estoy ahora", "dónde estoy ahora", "cerca del lugar donde estoy", "cerca del lugar dónde estoy",
	"en este lugar", "en éste lugar", "por mi ubicacion", "por mi ubicación", "en el sitio donde estoy", "en el sitio dónde estoy",
	"en este mismo lugar", "en éste mismo lugar", "por los alrededores",
	"en esta area geografica", "en esta area geográfica", "en esta área geografica",
	"en esta área geográfica", "en ésta area geografica", "en ésta area geográfica",
	"en ésta área geografica", "en ésta área geográfica",
	"cerca de mi posicion exacta", "cerca de mí posición exacta", "cerca de mí posicion exacta", "cerca de mi posición exacta",
	"en el entorno donde estoy", "en el entorno dónde estoy", "en mi lugar actual", "en mí lugar actual", "alrededor de este punto", "alrededor de éste punto",
	"donde me encuentro en este momento", "dónde me encuentro en éste momento", "dónde me encuentro en este momento", "donde me encuentro en éste momento",
	"en esta zona especifica", "en esta zona específica", "en ésta zona específica", "en ésta zona específica",
	"cerca de aqui mismo", "cerca de aquí mismo",
	"cerca de esta ubicacion exacta", "cerca de ésta ubicación exacta", "cerca de esta ubicación exacta", "cerca de ésta ubicacion exacta",
	"en las proximidades de aqui", "en las proximidades de aquí", "alrededor de donde me ubico", "alrededor de dónde me ubico",
	"en el area cercana a mi", "en el área cercana a mí", "en el área cercana a mi", "en el area cercana a mí",
	"en los alrededores de mi sitio", "en los alrededores de mí sitio",
	"alrededor de esta area", "alrededor de esta área", "alredeor de ésta area", "alrededor de ésta área",
	"cerca del lugar donde me encuentro", "cerca del lugar dónde me encuentro",
	"en mi ubicacion de ahora", "en mi ubicación de ahora", "alrededor de mi punto actual",
	"alrededor de mí punto actual", "en el lugar donde me ubico", "en el lugar dónde me ubico",
	"cerca de este punto exacto", "cerca de éste punto exacto",
	"en las cercanias donde estoy", "en las cercanías donde estoy", "en las cercanias dónde estoy", "en las cercanías dónde estoy",
	"en las cercanias de donde estoy", "en las cercanías de donde estoy", "en las cercanias de dónde estoy", "en las cercanías de dónde estoy",
	"alrededor de esta posicion", "alrededor de esta posición", "alrededor de ésta posicion", "alrededor de ésta posición",
	"dentro de mi radio", "dentro de mí radio", "en la vecindad de aqui", "en la vecindad de aquí",
	"en los alrededores inmediatos", "por donde estoy ahora", "por dónde estoy ahora",
	"cerca de este lugar preciso", "cerca de éste lugar preciso",
	"en las cercanias de esta posicion", "en las cercanias de esta posición", "en las cercanias de ésta posicion",
	"en las cercanias de ésta posición", "en las cercanías de esta posicion", "en las cercanías de esta posición",
	"en las cercanías de ésta posicion", "en las cercanías de ésta posición",
	"cerca del sitio donde estoy", "cerca del sitio dónde estoy",
	"en mi ubicacion especifica", "en mi ubicacion específica", "en mi ubicación especifica",
	"en mi ubicación específica", "en mí ubicacion especifica", "en mí ubicación específica",
	"en mi ubicación específica", "en mí ubicación específica",
	"por los alrededores donde me ubico", "por los alrededores dónde me ubico",
	"en este punto exacto", "en éste punto exacto", "por este punto exacto", "por éste punto exacto",
	"en la zona donde me encuentro", "en la zona dónde me encuentro", "en la proximidad donde estoy", "en la proximidad dónde estoy",
	"por la ubicacion actual", "por la ubicación actual", "en el sitio exacto donde estoy", "en el sitio exacto dónde estoy"
]
