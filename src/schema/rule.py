from typing import List

from pydantic import BaseModel

from src.schema import Channel


class RuleSettings(BaseModel):
    name: str
    telegram_channel_id: int
    channels: List[Channel]
