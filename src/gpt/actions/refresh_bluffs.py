import asyncio
import datetime as dt
import logging
import openai
import re
from typing import List
from beanie.operators import In, And
from db import create_client, start_beanie_session, get_db
from db.football import Match, Transfer, TransferType
from db.gpt import Bluff, Usage
import gpt.prompts.bluffball as bluffball
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_COUNTRIES = ("England", "Scotland", "Wales",)

def _get_gpt_response(content: str, base_prompt: str = bluffball.prompt):
    logger.debug(f"Getting GPT response for {content}")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"content": base_prompt, "role": "system"},
            {"role": "assistant", "content": content},
        ],
        max_tokens=500,
    )

    return response


def generate_from_prompt(
    content: str,
    base_prompt: str = bluffball.prompt,
) -> Bluff:
    logger.info(f"Generating bluff from prompt for {content}")
    response = _get_gpt_response(content=content, base_prompt=base_prompt)
    bluff = Bluff(
        message=response["choices"][0]["message"]["content"],
        date=dt.datetime.now(),
        usage=Usage(**response["usage"].to_dict()),
    )
    return bluff


async def get_matches(n=100, countries = DEFAULT_COUNTRIES, skip_youth: bool = True, bluffed_already: bool = False) -> List[Match]:
    await start_beanie_session()
    all_unbluffed_matches: List[Match] = await (
        Match
        .find(
            And(
                Match.bluffed == bluffed_already, 
                In(Match.country, countries)
            )
        )
        .to_list())
    logger.info(f"Got {len(all_unbluffed_matches)} matches from DB: countries={countries}, bluffed_already={bluffed_already}")

    if skip_youth:
        def has_youth(m: Match) -> bool:
            youth_regex = r"U[0-9]"
            has_comp = re.search(youth_regex, m.competition)
            has_home = re.search(youth_regex, m.homeTeam)
            has_away = re.search(youth_regex, m.awayTeam)
            return bool(has_comp or has_home or has_away)
        
        all_unbluffed_matches = [m for m in all_unbluffed_matches if not has_youth(m)]
        logger.info(f"Got {len(all_unbluffed_matches)} matches after filtering out youth matches")
    
    return all_unbluffed_matches[:n]


async def refresh_bluffs(n=100, countries = DEFAULT_COUNTRIES, skip_youth: bool = True):
    logger.debug("Refreshing bluffs")
    await start_beanie_session()
    transfers = await Transfer.find(Transfer.bluffed == False).to_list(length=10)
    logger.info(f"Got {len(transfers)} transfers")
    for t in transfers:
        if t.transferType != TransferType.done_deal:
            continue
        transfer_str = f"{t.playerName} from {t.oldClub} to {t.newClub} for {t.price}"
        bluff = generate_from_prompt(content=transfer_str)
        await Bluff.insert(bluff)
        await Transfer.set(t, {"bluffed": True})
    matches = await get_matches(n=n, countries=countries, skip_youth=skip_youth, bluffed_already=False)
    for m in matches:
        match_str = m.json()
        bluff = generate_from_prompt(content=match_str)
        await Bluff.insert(bluff)
        await Match.set(m, {"bluffed": True})
        logger.info("Finished refreshing {m}")
    logger.info("Finished refreshing bluffs")

if __name__ == "__main__":
    # b = 1
    # content = "{\n  \"headline\": \"Manchester United signs new striker\",\n  \"player\": \"Gareth Bale\",\n  \"club\": \"Real Madrid\",\n  \"fee\": \"$100 million\",\n  \"contract\": \"5-year deal\"\n}"
    # x = generate_from_prompt(content=content)
    # b =1
    asyncio.run(refresh_bluffs())
    # asyncio.run(get_matches(bluffed_already=True))
