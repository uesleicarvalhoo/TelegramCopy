from src.rules.base import BaseRule


class Rule(BaseRule):
    def parse_message(self, message: str) -> None:
        pair, direction, hour, obs1, obs2 = [x.strip() for x in self.remove_emoji(message).split("\n") if x][:5]
        self.pair = pair
        self.hour = hour
        self.signal = direction
        self.obs = "%s\n%s" % (obs1, obs2)

    def validate_signal(self) -> bool:
        return True

    def validate_message(self, message: str) -> bool:
        return "call" in message.lower() or "put" in message.lower()
