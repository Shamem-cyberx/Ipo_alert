"""
Daily U.S. IPO Alert – fetches IPOs from Finnhub and emails qualifying tickers (> $200M offer).

Run daily (e.g. 9 AM Dubai time) via Task Scheduler (Windows) or cron (Linux/Mac).
No cloud automation needed – free and self-hosted.
"""
import datetime

import pytz
import requests
import smtplib
from email.mime.text import MIMEText

from config import (
    API_KEY,
    EMAIL_PASSWORD,
    EMAIL_RECIPIENT,
    EMAIL_SENDER,
    MIN_OFFER_VALUE_USD,
    SEND_WHEN_EMPTY,
    SMTP_PORT,
    SMTP_SERVER,
    US_EXCHANGES,
)


def get_today_dubai():
    """Get today's date in YYYY-MM-DD format based on Dubai time zone (UTC+4)."""
    dubai_tz = pytz.timezone("Asia/Dubai")
    return datetime.datetime.now(dubai_tz).strftime("%Y-%m-%d")


def fetch_ipos(today):
    """Fetch IPO calendar data for today from Finnhub API."""
    url = f"https://finnhub.io/api/v1/calendar/ipo?from={today}&to={today}&token={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("ipoCalendar", [])
    print(f"API error: {response.status_code} - {response.text}")
    return []


def filter_qualifying_ipos(ipos):
    """Filter U.S. IPOs with totalSharesValue above configured minimum."""
    qualifying = []
    for ipo in ipos:
        exchange = ipo.get("exchange", "").lower()
        if any(ex in exchange for ex in US_EXCHANGES):
            if ipo.get("totalSharesValue", 0) > MIN_OFFER_VALUE_USD:
                qualifying.append(ipo.get("symbol", "Unknown"))
    return qualifying


def _build_email_body(tickers, today):
    """Build a neat, formatted email body."""
    min_m = MIN_OFFER_VALUE_USD // 1_000_000
    header = f"Daily U.S. IPO Alert\nDate: {today}\n"
    header += f"Criteria: U.S. exchanges, offer size > ${min_m}M\n"
    header += "-" * 40

    if tickers:
        body = f"{header}\n\nQualifying tickers today:\n\n"
        body += "\n".join(f"  • {t}" for t in tickers)
    else:
        body = f"{header}\n\nNo qualifying IPOs today."

    return body


def send_email(tickers, today):
    """Send email if there are qualifying tickers, or when SEND_WHEN_EMPTY is enabled."""
    if not tickers and not SEND_WHEN_EMPTY:
        print("No qualifying IPOs today - no email sent.")
        return

    body = _build_email_body(tickers, today)
    subject = "Daily U.S. IPO Alert - Qualifying Tickers" if tickers else "Daily U.S. IPO Alert - No Qualifying IPOs Today"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email sending failed: {e}")


def _check_config():
    """Warn if required credentials are missing."""
    missing = []
    if not API_KEY:
        missing.append("FINNHUB_API_KEY")
    if not EMAIL_SENDER:
        missing.append("EMAIL_SENDER")
    if not EMAIL_PASSWORD:
        missing.append("EMAIL_PASSWORD")
    if not EMAIL_RECIPIENT:
        missing.append("EMAIL_RECIPIENT")
    if missing:
        print("Missing config! Copy .env.example to .env and set:", ", ".join(missing))
        raise SystemExit(1)


if __name__ == "__main__":
    _check_config()
    today = get_today_dubai()
    print(f"Running for date: {today}")
    ipos = fetch_ipos(today)
    tickers = filter_qualifying_ipos(ipos)
    send_email(tickers, today)
