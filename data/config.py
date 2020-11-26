import os

from dotenv import load_dotenv

load_dotenv("/home/vadim/Documents/GitHub/gender_age_bot/.env.dist")

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins = [
    os.getenv("ADMIN_ID"),
]

ip = os.getenv("ip")
