import datetime as dt
from typing import Optional, Set
from beanie import Document, Indexed
from pydantic import BaseModel


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Bluff(Document):
    message: str
    date: Indexed(dt.datetime)
    usage: Usage
    country: Optional[str] = None
    team1: Optional[str] = None
    team2: Optional[str] = None
    cup: Optional[str] = None

    class Settings:
        bson_encoders = {
            dt.datetime: lambda d: dt.datetime(
                year=d.year, month=d.month, day=d.day, hour=d.hour, minute=d.minute, second=d.second
            )
        }
