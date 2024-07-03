import os
from pathlib import Path


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

# Logger variables
LOGGING_FORMAT: str = "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"

# Other variables
RGX_EMAIL: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Database variables
BASE_DIR: Path = Path(__file__).resolve().parent.parent
DB_PATH: str = os.path.join(BASE_DIR, "tiptrip.sqlite")
ADMIN_VALUES: list = ["admin", "admin", "admin"]
