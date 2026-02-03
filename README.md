# IPO Alert – Daily U.S. IPO Email Notifications

Fetches IPOs from Finnhub and emails qualifying U.S. tickers (offer > $200M). Runs locally – no cloud automation, no cost. Schedule with **Task Scheduler** (Windows) or **cron** (Linux/Mac).

> *Why this script?* Tools like Make.com and n8n can do this but add cost. This keeps it simple and free, and you control where it runs. See [PROJECT_STORY.md](PROJECT_STORY.md) for the full cost comparison and screenshots.

---

## Quick Start (clone and run)

### 1. Clone the repo

```bash
git clone https://github.com/Shamem-cyberx/Ipo_alert.git
cd Ipo_alert
```

### 2. Requirements

- Python 3.8+
- Finnhub API key (free): https://finnhub.io/
- Gmail (or other SMTP) – for Gmail use an [App Password](https://myaccount.google.com/apppasswords), not your normal password

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure credentials

**Windows:**
```bash
copy .env.example .env
```

**Linux / Mac:**
```bash
cp .env.example .env
```

Edit `.env` and add your values (never commit `.env`):

| Variable | Description |
|----------|-------------|
| `FINNHUB_API_KEY` | From https://finnhub.io/ (free) |
| `EMAIL_SENDER` | Your Gmail address |
| `EMAIL_PASSWORD` | Gmail App Password (not regular password) |
| `EMAIL_RECIPIENT` | Where to receive alerts |

Optional:

- `SMTP_SERVER`, `SMTP_PORT` – defaults work for Gmail
- `MIN_OFFER_VALUE_USD` – default 200000000 ($200M)
- `SEND_WHEN_EMPTY` – set to `true` to receive an email even when no qualifying IPOs (default: false)

### 5. Run once

```bash
python ipo_alert.py
```

You should see `Running for date: YYYY-MM-DD` and either `Email sent successfully!` or `No qualifying IPOs today – no email sent.`

---

## Scheduling

### Windows – Task Scheduler

1. Open **Task Scheduler** → Create Basic Task
2. **Name:** IPO Alert
3. **Trigger:** Daily at 9:00 AM (or your preferred time, e.g. Dubai 9 AM)
4. **Action:** Start a program
   - **Program:** `C:\Path\To\Python\python.exe` (or `py`)
   - **Arguments:** `C:\Path\To\Ipo_alert\ipo_alert.py`
   - **Start in:** `C:\Path\To\Ipo_alert`
5. Finish and test: right‑click task → Run

> Ensure the `.env` file is in the same folder as `ipo_alert.py` so credentials load correctly.

### Linux / Mac – cron

```bash
crontab -e
```

Add (runs daily at 9:00 AM, adjust path and time as needed):

```bash
0 9 * * * cd /path/to/Ipo_alert && /usr/bin/python3 ipo_alert.py
```

Or use a virtual environment:

```bash
0 9 * * * cd /path/to/Ipo_alert && ./venv/bin/python ipo_alert.py
```

---

## Project layout

```
Ipo_alert/
├── ipo_alert.py       # Main script
├── config.py          # Loads settings from .env
├── .env.example       # Template – copy to .env and fill in
├── .env               # Your credentials (gitignored)
├── requirements.txt
├── README.md          # Setup guide
├── PROJECT_STORY.md   # Cost comparison & screenshots
├── WORKFLOW.md        # Detailed workflow
└── assets/            # Screenshots for docs
```

---

## Notes

- **Timezone:** IPO date is based on Dubai time (UTC+4)
- **Alternatives:** Make.com / n8n can automate this but add cost. This script is free and works with any scheduler
- **Security:** Keep `.env` private; it is gitignored
