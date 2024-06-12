import os
from pathlib import Path


# Project details
PROJECT_NAME: str = "Poli-GAS"
STATIONARY_PRICE: float = 15.99
TANK_PRICE: float = 21.99

PROJECT_NAME_SIZE: int = 45
TITLE_SIZE: int = 30
TEXT_SIZE: int = 15


# Device dimensions
APP_WIDTH: int = 400
APP_HEIGHT: int = 750

# Components dimensions
EXTERIOR_PADDING: int = 35
COMPONENTS_WIDTH: int = APP_WIDTH - (EXTERIOR_PADDING * 2)

APP_BAR_HEIGHT: int = 50

# Database variables
BASE_DIR: Path = Path(__file__).resolve().parent.parent
DB_PATH: str = os.path.join(BASE_DIR, "users.sqlite")
ADMIN_VALUES: list = ["admin", "admin", "admin"]

# Logger variables
LOGGING_FORMAT: str = "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
