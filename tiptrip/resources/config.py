import os
from pathlib import Path


# Names
PROJECT_NAME: str = "TIP TRIP"
BOT_NAME: str = "Bot"

# Colors
MAIN_COLOR: str = "#FF7F11"  # orange
SECONDARY_COLOR: str = "#006E7E"  # blue

# Device dimensions
APP_WIDTH: int = 333  # px
APP_HEIGHT: int = 700  # px
WINDOW_HEADER: int = 39  # px
HEIGHT_PLUS_HEADER: int = APP_HEIGHT + WINDOW_HEADER

# RESOLUCIÓN FULL HD+
# width:  1080 - 332.55
# height: 2400 - 739

# Components variables
RADIUS: int = 20  # px
BLUR: int = 10  # px
LOW_BLUR: int = 7  # px
SPACING: int = 20  # px

# Database variables
BASE_DIR: Path = Path(__file__).resolve().parent.parent
DB_PATH: str = os.path.join(BASE_DIR, "tiptrip.sqlite")
ADMIN_VALUES: list = ["admin", "admin", "admin"]

# Logger variables
LOGGING_FORMAT: str = "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"

# Other variables
RGX_EMAIL: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
