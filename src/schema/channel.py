from pydantic import BaseModel


class Channel(BaseModel):
    id: int
    group_name: str
