import json

from decouple import config

from src.schema import RuleSettings

API_HASH = config("API_HASH")
API_TOKEN = config("API_TOKEN", cast=int)
TELEGRAM_BOT_API_KEY = config("TELEGRAM_BOT_API_KEY")
TELEGRAM_STRING_SESSION = config("TELEGRAM_STRING_SESSION")

with open("settings.json", "r", encoding="utf-8") as f:
    RULE_SETTINGS = json.load(f)


CHANNEL_ID_TO_SETTINGS = {
    value["telegram_channel_id"]: RuleSettings(**{**value, "name": key}) for key, value in RULE_SETTINGS.items()
}
