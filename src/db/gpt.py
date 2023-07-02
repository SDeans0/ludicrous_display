import datetime as dt
from beanie import Document
from pydantic import BaseModel


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Bluff(Document):
    message: str
    date: dt.date
    usage: Usage

    class Settings:
        bson_encoders = {
            dt.date: lambda d: dt.datetime(
                year=d.year, month=d.month, day=d.day, hour=0, minute=0, second=0
            )
        }
