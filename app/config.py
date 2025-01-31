# /app/config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Define the absolute path for the static folder
STATIC_DIR = BASE_DIR / "static"
IDEA_ATTACHMENTS_DIR = STATIC_DIR / "ideas-attachments"

# Ensure the directories exist
STATIC_DIR.mkdir(parents=False, exist_ok=True)
IDEA_ATTACHMENTS_DIR.mkdir(parents=False, exist_ok=True)