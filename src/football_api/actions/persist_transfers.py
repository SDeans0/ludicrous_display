from typing import Tuple
import asyncio
import datetime as dt
import logging
import os
from db import start_beanie_session
from db.football import Transfer
from football_api.client.client import SimpleFootballApiClient

logger = logging.getLogger(__name__)


async def get_and_persist_transfers(leagues: Tuple[str] = ("premierleague","thechampionship", "leagueone","leaguetwo")):
    """
    Get transfers from the api and persist them in the database
    """
    api_key = os.environ.get("RAPID_API_KEY")
    client = SimpleFootballApiClient(api_key=api_key)
    now = dt.datetime.now()
    for league in leagues:
        transfers = client.get_transfers(chamionship=league)
        for transfer in transfers:
            try:
                await Transfer.insert_one(Transfer(date_added=now,**transfer))
            except Exception as e:
                logger.exception(e)

async def async_main():
    await start_beanie_session()
    await get_and_persist_transfers()

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    
    main()