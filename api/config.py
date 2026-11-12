"""Configuración de la suite, leída de variables de entorno."""
import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com").rstrip("/")
TIMEOUT = float(os.getenv("API_TIMEOUT", "10"))
