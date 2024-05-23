import os
from pathlib import Path


# Device dimensions
APP_WIDTH: int = 400
APP_HEIGHT: int = 750

# Components dimensions
EXTERIOR_PADDING: int = 50
COMPONENTS_WIDTH: int = APP_WIDTH - (EXTERIOR_PADDING * 2)

APP_BAR_HEIGHT = 50

# Database variables
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.path.join(BASE_DIR, "sites.sqlite")

# Project details
PROJECT_NAME = "Tip Trip"
