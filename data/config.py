import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
print(BOT_TOKEN)
admins = [
    os.getenv("ADMIN_ID"),
]

ip = os.getenv("ip")
host = os.getenv("PGHOST")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")