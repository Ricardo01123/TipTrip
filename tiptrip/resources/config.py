import os


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

# Other variables
LOGGING_FORMAT: str = "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
RGX_EMAIL: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Back-End API
BACK_END_URL: str = "http://127.0.0.1:5000"
GET_DEMO_DATA_ENDPOINT: str = "get_demo_data"
GET_RECORD_ENDPOINT: str = "get_record"
ADD_USER_ENDPOINT: str = "add_user"
AUTH_USER_ENDPOINT: str = "auth_user"

# Speech recognition
SAMPLING_RATE: int = 16_000
CHANNELS: int = 1
FRAMES_PER_BUFFER: int = 8_192
FRAMES_FLOW: int = 4_096
CUTOFF: int = 3_000
ORDER: int = 6

PROJECT_DIR_ABSPATH: str = os.getcwd()
MODELS_ABSPATH: str = os.path.join(PROJECT_DIR_ABSPATH, "models")
VOSK_ABSPATH: str = os.path.join(MODELS_ABSPATH, "vosk-model-small-es-0.42")
# MODEL_ABS_PATH: str = r"D:\Todo\ESCOM\Clases\TT\tt_codes\TipTrip\tiptrip\models\vosk-model-small-es-0.42"
