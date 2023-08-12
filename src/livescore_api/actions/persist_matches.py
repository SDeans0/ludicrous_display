import asyncio
import datetime as dt
import os
import logging
from typing import List, Tuple
from db import start_beanie_session

from db.football import Match, Score
from livescore_api.client.client import LiveScoreApiClient
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_and_persist_fixtures(leagues: Tuple[str] = ("premierleague","thechampionship", "leagueone","leaguetwo")):
    """
    Get fixtures from the api and persist them in the database
    """
    api_key = os.environ.get("RAPID_API_KEY")
    client = LiveScoreApiClient(api_key=api_key)
    logger.info("Getting fixtures from api")
    fixtures = client.get_matches()
    logger.info("Converting fixtures to matches")
    matches = convert_fixture(fixtures)
    # try:
    #     await Match.insert_many(matches)
    # except Exception as e:
    #     logger.exception(e)


def convert_fixture(fixture: dict, included_leagues: Tuple[str] = ("Premier League","Community Shield", "League One","FA Cup", "Championship", "League Two", "EFL Cup", "FA Women's Super League", "Women's FA Cup", "Women's World Cup", "Cymru Premier", "World Cup")) -> List[Match]:
    """
    Convert the fixture dictionary from the api into list of match objects
    """
    output: List[Match] = []

    for stage in fixture["Stages"]:
        if (comp:=stage.get("CompN")) not in included_leagues:
            logger.info(f"Skipping {comp} in country {stage['Cnm']}")
            continue
        logger.info(f"Converting {comp}")
        for event in stage["Events"]:
            # example event structure, for a match between home team burnley and away team man city:
            # {'Eid': '968063', 'Pids': {'12': 'SBTE_29018274', '8': '968063'}, 'Tr1': '0', 'Tr2': '3', 'Trh1': '0', 'Trh2': '2', 'Tr1OR': '0', 'Tr2OR': '3', 'T1': [{...}], 'T2': [{...}], 'Eps': 'FT', 'Esid': 6, 'Epr': 2, 'Ecov': 0, ...}
            logger.info(f"Converting {event['T1'][0]['Nm']} vs {event['T2'][0]['Nm']}")
            output.append(Match(
                homeTeam=event["T1"][0]["Nm"],
                awayTeam=event["T2"][0]["Nm"],
                full_time_score=Score(
                    homeTeamScore=event["Tr1"],
                    awayTeamScore=event["Tr2"],
                ),
                half_time_score=Score(
                    homeTeamScore=event["Trh1"],
                    awayTeamScore=event["Trh2"],
                ),
                penalty_score=Score(
                    homeTeamScore=event["Trp1"],
                    awayTeamScore=event["Trp2"],
                ) if "Trp1" in event else None,
                competition=stage.get("CompN"),
                country=stage["Cnm"], 
                date=dt.date.today().isoformat(),
                date_added=dt.datetime.now(),
                bluffed=False,
            ))
    return output

async def async_main():
    await start_beanie_session()
    await get_and_persist_fixtures()

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()

    