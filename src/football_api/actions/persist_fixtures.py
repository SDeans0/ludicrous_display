import asyncio
import datetime as dt
import os
import logging
from typing import Tuple

from db.football import Match
from football_api.client.client import SimpleFootballApiClient

logger = logging.getLogger(__name__)


async def get_and_persist_fixtures(leagues: Tuple[str] = ("premierleague","thechampionship", "leagueone","leaguetwo")):
    """
    Get fixtures from the api and persist them in the database
    """
    api_key = os.environ.get("RAPID_API_KEY")
    client = SimpleFootballApiClient(api_key=api_key)
    now = dt.datetime.now()
    for league in leagues:
        fixtures = client.get_fixtures(chamionship=league)
        for fixture in fixtures:
            if not fixture:
                continue
            try:
                await Match.insert_one(Match(date_added=now, **fixture))
            except Exception as e:
                logger.exception(e)


def main():
    asyncio.run(get_and_persist_fixtures())

if __name__ == "__main__":
    main()