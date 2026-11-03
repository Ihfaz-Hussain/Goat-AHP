import os
import psycopg2
from dotenv import load_dotenv

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"
if not ENV_PATH.is_file():
    ENV_PATH = PROJECT_ROOT / "src" / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

def get_connection():
    """Create a connection to the GOAT-AHP database."""

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
