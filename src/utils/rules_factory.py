from contextlib import suppress
from importlib import import_module
from typing import Union

from src.rules.base import BaseRule
from src.settings import CHANNEL_ID_TO_SETTINGS
from src.utils.logger import logger


def load_rule(channel_id: str) -> Union[BaseRule, None]:
    if rule_settings := CHANNEL_ID_TO_SETTINGS.get(channel_id):
        with suppress(ModuleNotFoundError, ImportError):
            imported_module = import_module(f".{rule_settings.name}", package="src.rules")
            return getattr(imported_module, "Signal")(rule_settings.channels)

    logger.warning("ChannelID %s not found, ignored." % channel_id)
    return None
