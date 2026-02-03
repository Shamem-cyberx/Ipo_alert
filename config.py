"""Load configuration from environment variables. Never commit .env with real credentials."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

# API
API_KEY = os.getenv("FINNHUB_API_KEY", "")

# Email (Gmail example – use app password, not regular password)
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# Filter: U.S. exchanges, minimum offer size in USD
US_EXCHANGES = ["nasdaq", "nyse", "amex"]
MIN_OFFER_VALUE_USD = int(os.getenv("MIN_OFFER_VALUE_USD", "200000000"))  # $200M default

# Send email even when no qualifying IPOs (set to "true" to enable)
SEND_WHEN_EMPTY = os.getenv("SEND_WHEN_EMPTY", "false").lower() in ("true", "1", "yes")
