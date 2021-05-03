from src.rules.base import BaseRule


class Rule(BaseRule):
    def parse_message(self, message: str) -> None:
        self.__base_message = message.replace("Corujão 24hs", "%(group_name)s")

    def validate_signal(self) -> bool:
        return True

    @property
    def base_message(self) -> str:
        return self.__base_message

    def validate_message(self, message: str) -> bool:
        return True
