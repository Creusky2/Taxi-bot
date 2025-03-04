import pytz
from datetime import datetime, timedelta

DISCORD_CHANNEL_FACTURES = 1218274316291018772
DISCORD_CHANNEL_MISSIONS = 1218274512248901714

import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables d'environnement

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


PARIS_TZ = pytz.timezone("Europe/Paris")

def get_week_date_range():
    now = datetime.now(PARIS_TZ)
    start_of_week = now - timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute, seconds=now.second)
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
    return start_of_week.astimezone(pytz.utc), end_of_week.astimezone(pytz.utc)
