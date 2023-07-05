import datetime as dt
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

    class Settings:
        bson_encoders = {
            dt.datetime: lambda d: dt.datetime(
                year=d.year, month=d.month, day=d.day, hour=d.hour, minute=d.minute, second=d.second
            )
        }
