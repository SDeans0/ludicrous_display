import datetime as dt
from enum import Enum
from typing import Optional
from beanie import Document, Indexed
from pydantic import BaseModel, Extra


class TransferType(str, Enum):
    done_deal = "DONE DEAL"
    loan = "LOAN"
    free_transfer = "FREE TRANSFER"
    contract_extension = "CONTRACT EXTENSION"
    contract_termination = "CONTRACT TERMINATION"
    contract = "CONTRACT"
    loan_return = "LOAN RETURN"
    loan_extension = "LOAN EXTENSION"


class BaseNews(BaseModel):
    date_added: dt.datetime
    bluffed: bool = False


class Transfer(Document, BaseNews):
    transferType: TransferType
    transferDate: str
    playerName: str
    playerRole: str
    oldClub: str
    newClub: str
    price: str
    renewal: str
    league: Optional[str]

    class Settings:
        bson_encoders = {
            dt.datetime: lambda d: dt.datetime(
                year=d.year,
                month=d.month,
                day=d.day,
                hour=d.hour,
                minute=d.minute,
                second=d.second,
            )
        }


class Score(BaseModel):
    homeTeamScore: str
    awayTeamScore: str


class Match(Document, BaseNews, extra = Extra.ignore):
    """Class for persisting fixture data"""
    homeTeam: str
    awayTeam: str
    full_time_score: Optional[Score]
    half_time_score: Optional[Score]
    penalty_score: Optional[Score]
    competition: str
    date: str
    country: str
