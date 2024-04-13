import asyncio
import datetime as dt
import logging
import openai
from db import create_client, start_beanie_session, get_db
from db.football import Match, Transfer, TransferType
from db.gpt import Bluff, Usage
import gpt.prompts.bluffball as bluffball
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_gpt_response(content: str, base_prompt: str = bluffball.prompt):
    logger.debug(f"Getting GPT response for {content}")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"content": base_prompt, "role": "system"},
            {"role": "assistant", "content": content},
        ],
        max_tokens=1000,
    )

    return response


def generate_from_prompt(
    content: str,
    base_prompt: str = bluffball.prompt,
) -> Bluff:
    logger.debug(f"Generating bluff from prompt for {content}")
    response = _get_gpt_response(content=content, base_prompt=base_prompt)
    bluff = Bluff(
        message=response["choices"][0]["message"]["content"],
        date=dt.datetime.now(),
        usage=Usage(**response["usage"].to_dict()),
    )
    return bluff


async def refresh_bluffs():
    logger.debug("Refreshing bluffs")
    bluffs = []
    await start_beanie_session()
    transfers = await Transfer.find(Transfer.bluffed == False).to_list(length=10)
    logger.info(f"Got {len(transfers)} transfers")
    for t in transfers:
        if t.transferType != TransferType.done_deal:
            continue
        transfer_str = f"{t.playerName} from {t.oldClub} to {t.newClub} for {t.price}"
        next_bluff = generate_from_prompt(content=transfer_str)
        next_bluff.team1 = t.oldClub
        next_bluff.team2 = t.newClub
        bluffs.append(next_bluff)
        await Transfer.set(t, {"bluffed": True})
    matches = await Match.find(Match.bluffed == False).to_list(length=100)
    logger.info(f"Got {len(matches)} matches")
    for m in matches:
        match_str = m.json()
        next_bluff = generate_from_prompt(content=transfer_str)
        next_bluff.team1 = m.homeTeam
        next_bluff.team2 = m.awayTeam
        next_bluff.cup = m.competition
        next_bluff.country = m.country
        bluffs.append(next_bluff)
        await Match.set(m, {"bluffed": True})
    if bluffs:
        logger.info(f"Inserting {len(bluffs)} bluffs")
        await Bluff.insert_many(bluffs)


if __name__ == "__main__":
    # b = 1
    # content = "{\n  \"headline\": \"Manchester United signs new striker\",\n  \"player\": \"Gareth Bale\",\n  \"club\": \"Real Madrid\",\n  \"fee\": \"$100 million\",\n  \"contract\": \"5-year deal\"\n}"
    # x = generate_from_prompt(content=content)
    # b =1
    asyncio.run(refresh_bluffs())
