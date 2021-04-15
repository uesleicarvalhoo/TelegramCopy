from typing import Dict

from src.rules.base import BaseSignal
from src.settings import CHANNEL_ID_METODO_CONSISTENTE, CHANNEL_ID_METODO_CONSISTENTE_NOVO, CHANNEL_ID_METODO_CONSISTENTE_V2

ALLOWED_MESSAGES = ("WIN GALE", "WIN SEM GALE", "LOSS", "PLACAR DIÁRIO")


class Signal(BaseSignal):
    def parse_message(self, message: str) -> None:
        self.__base_message = message.replace("COMUNIDADE JEDI", "%(group_name)s")

    def validate_signal(self) -> bool:
        return True

    @property
    def base_message(self) -> str:
        return self.__base_message

    def validate_message(self, message: str) -> bool:
        return "MOEDA" in message and "OPERAÇÃO" in message or any(x in message for x in ALLOWED_MESSAGES)

    @property
    def channels_messages(self) -> Dict:
        return {
            CHANNEL_ID_METODO_CONSISTENTE: self.base_message % {"group_name": "MÉTODO CONSISTENTE"},
            CHANNEL_ID_METODO_CONSISTENTE_NOVO: self.base_message % {"group_name": "MÉTODO CONSISTENTE"},
            CHANNEL_ID_METODO_CONSISTENTE_V2: self.base_message % {"group_name": "MÉTODO CONSISTENTE"},
        }
