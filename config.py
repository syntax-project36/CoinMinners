import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
ADMIN_ID = os.getenv("ADMIN_ID")

CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
GROUP_USERNAME = os.getenv("GROUP_USERNAME")