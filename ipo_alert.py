import requests
import datetime
import smtplib
from email.mime.text import MIMEText
import pytz  # For time zone handling

# Configuration - Replace with your details
API_KEY = 'd6097v1r01qihi8oudvgd6097v1r01qihi8oue00'  # Your Finnhub API key
EMAIL_SENDER = 'shamem0801@gmail.com'  # e.g., your Gmail address
EMAIL_PASSWORD = 'wmlm nzfj awhn reul'  # Gmail app password (not regular password)
EMAIL_RECIPIENT = 'shamem0801@gmail.com'  # Your email to receive alerts
SMTP_SERVER = 'smtp.gmail.com'  # For Gmail; change for other providers like Outlook
SMTP_PORT = 587

# U.S. exchanges to filter (case-insensitive match)
US_EXCHANGES = ['nasdaq', 'nyse', 'amex']

def get_today_dubai():
    """Get today's date in YYYY-MM-DD format based on Dubai time zone (UTC+4)."""
    dubai_tz = pytz.timezone('Asia/Dubai')
    today = datetime.datetime.now(dubai_tz).strftime('%Y-%m-%d')
    return today

def fetch_ipos(today):
    """Fetch IPO calendar data for today from Finnhub API."""
    url = f'https://finnhub.io/api/v1/calendar/ipo?from={today}&to={today}&token={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('ipoCalendar', [])
    else:
        print(f"API error: {response.status_code} - {response.text}")
        return []

def filter_qualifying_ipos(ipos):
    """Filter U.S. IPOs with totalSharesValue > $200 million."""
    qualifying_tickers = []
    for ipo in ipos:
        exchange_lower = ipo.get('exchange', '').lower()
        if any(us_ex in exchange_lower for us_ex in US_EXCHANGES):
            total_value = ipo.get('totalSharesValue', 0)
            if total_value > 200000000:  # > $200M USD
                ticker = ipo.get('symbol', 'Unknown')
                qualifying_tickers.append(ticker)
    return qualifying_tickers

def send_email(tickers):
    """Send email ONLY if there are qualifying tickers."""
    if not tickers:
        print("No qualifying IPOs today - no email sent.")
        return  # Exit without sending
    
    body = f"Qualifying IPO tickers (> $200M offer amount) on U.S. markets today: {', '.join(tickers)}"
    
    msg = MIMEText(body)
    msg['Subject'] = 'Daily U.S. IPO Alert - Qualifying Tickers'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECIPIENT

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email sending failed: {str(e)}")

# Main execution (run this script daily at 9 AM Dubai time)
if __name__ == "__main__":
    today = get_today_dubai()
    print(f"Running for date: {today}")
    ipos = fetch_ipos(today)
    qualifying_tickers = filter_qualifying_ipos(ipos)
    send_email(qualifying_tickers)