import os

class Config:
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHANNELS = list(map(int, os.getenv("CHANNELS").split(',')))  # Comma-separated list of channel IDs
    ADMINS = list(map(int, os.getenv("ADMINS").split(',')))  # Comma-separated list of admin user IDs
    DATABASE_URI = os.getenv("DATABASE_URI")
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))
    PORT = int(os.getenv("PORT", 8000))  # Health check port for Koyeb
