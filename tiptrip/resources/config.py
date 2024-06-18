import os
from pathlib import Path


# Titles
PROJECT_NAME: str = "TIP TRIP"

# Titles sizes
PROJECT_NAME_SIZE: int = 45
TITLE_SIZE: int = 30
TEXT_SIZE: int = 15

DIALOG_TITLE_SIZE: int = TEXT_SIZE + 3

# Colors
MAIN_COLOR: str = "#FF7F11"  # orange
SECONDARY_COLOR: str = "#006E7E"  # blue

# Device dimensions
WINDOW_HEADER: int = 39
TOTAL_WIDTH: int = 350
TOTAL_HEIGHT: int = 700 + WINDOW_HEADER
HEIGHT_WITHOUT_HEADER: int = TOTAL_HEIGHT - WINDOW_HEADER

# Components dimensions
APP_BAR_HEIGHT: int = 50  # 0.0714285 % -> 50 px
PADDING: int = 20  # 0.0285714 % -> 20 px
MARGIN: int = 15  # 0.0214285 % -> 15 px

# Components variables
RADIUS: int = 20  # px
BLUR: int = 10  # px

# Database variables
BASE_DIR: Path = Path(__file__).resolve().parent.parent
DB_PATH: str = os.path.join(BASE_DIR, "tiptrip.sqlite")
ADMIN_VALUES: list = ["admin", "admin", "admin"]

# Logger variables
LOGGING_FORMAT: str = "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"

# Other variables
RGX_EMAIL: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# RESOLUCIÓN FULL HD+
# width:  1080 - 350
# height: 2400 - 778
