import datetime as dt
from enum import Enum
from typing import Optional
from beanie import Document, Indexed
from pydantic import BaseModel


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
    date_added: dt.date
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


class Match(Document, BaseNews):
    homeTeam: str
    awayTeam: str
    homeTeamScore: str
    awayTeamScore: str
