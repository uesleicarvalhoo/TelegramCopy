import re
from abc import abstractclassmethod
from typing import Dict, List

from src.schema import Channel


class BaseRule:
    pair: str = None
    hour: str = None
    obs: str = None
    signal: str = None
    timeframe: str = None
    channels: List[Channel]
    __base_message: str = None

    def __init__(self, channels_data: List[Channel]) -> None:
        self.channels = channels_data

    @abstractclassmethod
    def parse_message(self, message: str):
        raise NotImplementedError("Method parse_message must be implemented!")

    @abstractclassmethod
    def validate_message(self, message: str) -> bool:
        raise NotImplementedError("Method validated_message must be implemented!")

    def filter_signal(self, signal: str):
        signal = self.__remove_emoji(signal)
        signal = re.sub('ACIMA', 'CALL', signal)
        signal = re.sub('ABAIXO', 'PUT', signal)

        return signal

    def validate_signal(self) -> bool:
        return self.pair and self.hour and self.signal

    def remove_emoji(self, string: str) -> str:
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE,
        )

        return emoji_pattern.sub(r'', string)

    @property
    def base_message(self) -> str:
        return (
            f"✳️  %(group_name)s ✳️"
            f"\n📊 Ativo: {self.pair}"
            f"\n🔴 Direção: {self.signal}"
            f"\n⏰ Horário: {self.hour}"
            f"\n⏳ Timeframe: {self.timeframe}"
            if self.timeframe
            else "" "\n------------------"
            if self.obs
            else "" f"\n⚠️ {self.obs}"
            if self.obs
            else ""
        )

    @property
    def channels_messages(self) -> Dict:
        return {channel.id: self.base_message % channel.dict() for channel in self.channels}
