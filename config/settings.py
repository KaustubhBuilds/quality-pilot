import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8069")
    ODOO_DB: str = os.getenv("ODOO_DB", "quality_pilot_db")
    ODOO_USER: str = os.getenv("ODOO_USER", "admin")
    ODOO_PASSWORD: str = os.getenv("ODOO_PASSWORD", "admin")
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30000"))
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")


settings = Settings()
