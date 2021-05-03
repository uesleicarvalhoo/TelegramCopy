from src.rules.base import BaseRule

ALLOWED_MESSAGES = ("WIN GALE", "WIN SEM GALE", "LOSS", "PLACAR DIÁRIO")


class Rule(BaseRule):
    def parse_message(self, message: str) -> None:
        self.__base_message = message.replace("COMUNIDADE JEDI", "%(group_name)s")

    def validate_signal(self) -> bool:
        return True

    @property
    def base_message(self) -> str:
        return self.__base_message

    def validate_message(self, message: str) -> bool:
        return "MOEDA" in message and "OPERAÇÃO" in message or any(x in message for x in ALLOWED_MESSAGES)
