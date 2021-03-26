from contextlib import suppress
from importlib import import_module
from typing import Union

from src.rules.base import BaseSignal
from src.settings import CHANNEL_ID_TO_NAME
from src.utils.logger import logger


def load_signal(channel_id: str) -> Union[BaseSignal, None]:
    if module_name := CHANNEL_ID_TO_NAME.get(channel_id):
        with suppress(ModuleNotFoundError, ImportError):
            imported_module = import_module(f".{module_name}", package="src.rules")
            return getattr(imported_module, "Signal")()

    logger.info("ChannelID %s not found, ignored." % channel_id)
    return None
