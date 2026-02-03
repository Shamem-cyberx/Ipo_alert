# IPO Alert – Detailed Workflow

End-to-end flow from trigger to email delivery.

---

## Workflow Overview

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  Scheduler          │     │  Python Script      │     │  External Services  │
│  (Task Scheduler    │────▶│  ipo_alert.py       │────▶│  Finnhub API        │
│   or cron)          │     │                     │     │  SMTP (Gmail)       │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
         │                            │                            │
         │  Runs daily                │  Fetches & filters         │  Sends email
         │  (e.g. 10:30 AM)           │  IPOs                      │  to recipient
         └────────────────────────────┴────────────────────────────┘
```

---

## Step-by-Step Flow

### 1. Trigger
- **Task Scheduler** (Windows) or **cron** (Linux/Mac) runs `python ipo_alert.py` at the scheduled time (e.g. 10:30 AM daily).
- Working directory must be the project folder so `.env` and `config.py` are found.

### 2. Load Configuration
- `config.py` loads credentials from `.env` (API key, email, SMTP settings).
- Validates required variables: `FINNHUB_API_KEY`, `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECIPIENT`.
- Exits with clear error if any are missing.

### 3. Get Today's Date (Dubai Timezone)
- Uses `pytz` to get current date in **Asia/Dubai (UTC+4)**.
- Formats as `YYYY-MM-DD` for API and email.

### 4. Fetch IPO Calendar
- Calls Finnhub API:  
  `GET https://finnhub.io/api/v1/calendar/ipo?from={date}&to={date}&token={API_KEY}`
- Parses `ipoCalendar` from JSON response.
- Logs API errors if request fails.

### 5. Filter Qualifying IPOs
- **Exchange filter:** Only U.S. exchanges (NASDAQ, NYSE, AMEX).
- **Size filter:** `totalSharesValue` > `MIN_OFFER_VALUE_USD` (default $200M).
- Returns list of qualifying ticker symbols.

### 6. Build Email
- **Header:** Date, criteria (U.S. exchanges, > $200M).
- **Body (qualifying tickers):** Bullet list of tickers.
- **Body (no qualifying):** “No qualifying IPOs today.”
- **Subject:**
  - With tickers: `Daily U.S. IPO Alert - Qualifying Tickers`
  - Without tickers: `Daily U.S. IPO Alert - No Qualifying IPOs Today` (only if `SEND_WHEN_EMPTY=true`).

### 7. Send Email (or Skip)
- **Skip:** No tickers and `SEND_WHEN_EMPTY=false` → no email, script exits.
- **Send:** Connects to SMTP (Gmail default), authenticates with App Password, sends email to `EMAIL_RECIPIENT`.
- Logs success or failure.

### 8. Exit
- Script finishes. Scheduler records run result (e.g. 0x0 = success).

---

## Data Flow

| Step | Input | Output |
|------|-------|--------|
| 1. Trigger | Schedule time | `ipo_alert.py` executed |
| 2. Config | `.env` file | API key, email credentials, filters |
| 3. Date | System time + Dubai TZ | `YYYY-MM-DD` string |
| 4. Fetch | Date + API key | `ipoCalendar` list (raw IPOs) |
| 5. Filter | Raw IPOs, US_EXCHANGES, MIN_OFFER_VALUE_USD | List of qualifying tickers |
| 6. Build | Tickers, date | Email subject + body |
| 7. Send | Email content, SMTP credentials | Email delivered to recipient |

---

## File Roles

| File | Role |
|------|------|
| `ipo_alert.py` | Main entry point; orchestrates fetch → filter → email |
| `config.py` | Loads `.env`; exposes API_KEY, email, SMTP, filter settings |
| `.env` | Secrets (gitignored); never committed |
| `.env.example` | Template for required variables |
| `requirements.txt` | Python dependencies (requests, pytz, python-dotenv) |

---

## Dependencies

```
Scheduler (OS)  →  Python 3.8+  →  ipo_alert.py
                                        │
                                        ├── config.py (reads .env)
                                        ├── requests (Finnhub API)
                                        ├── pytz (timezone)
                                        └── smtplib (built-in, email)
```
