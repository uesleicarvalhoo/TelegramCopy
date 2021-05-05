import json
from typing import Union

from decouple import config

from src.schema import RuleSettings


def _normalize_log_level(level: str) -> Union[str, int]:
    try:
        return int(level)

    except ValueError:
        return level.upper()


API_HASH = config("API_HASH")
API_TOKEN = config("API_TOKEN", cast=int)
TELEGRAM_BOT_API_KEY = config("TELEGRAM_BOT_API_KEY")
TELEGRAM_STRING_SESSION = config("TELEGRAM_STRING_SESSION")
LOG_LEVEL = config("LOG_LEVEL", default="info", cast=_normalize_log_level)

with open("settings.json", "r", encoding="utf-8") as f:
    RULE_SETTINGS = json.load(f)


CHANNEL_ID_TO_SETTINGS = {
    value["telegram_channel_id"]: RuleSettings(**{**value, "name": key}) for key, value in RULE_SETTINGS.items()
}
