import asyncio
import datetime as dt
import openai
from db import create_client, start_beanie_session, get_db
from db.football import Transfer, TransferType
from db.gpt import Bluff, Usage
import gpt.prompts.bluffball as bluffball


def _get_gpt_response(content: str, base_prompt: str = bluffball.prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
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
    response = _get_gpt_response(content=content, base_prompt=base_prompt)
    bluff = Bluff(
        message=response["choices"][0]["message"]["content"],
        date=dt.datetime.now(),
        usage=Usage(**response["usage"].to_dict()),
    )
    return bluff


async def refresh_bluffs():
    bluffs = []
    await start_beanie_session()
    transfers = await Transfer.find(Transfer.bluffed == False).to_list(length=100)
    for t in transfers:
        if t.transferType != TransferType.done_deal:
            continue
        transfer_str = f"{t.playerName} from {t.oldClub} to {t.newClub} for {t.price}"
        bluffs.append(generate_from_prompt(content=transfer_str))
        await Transfer.set(t, {"bluffed": True})
    if bluffs:
        await Bluff.insert_many(bluffs)


if __name__ == "__main__":
    # b = 1
    # content = "{\n  \"headline\": \"Manchester United signs new striker\",\n  \"player\": \"Gareth Bale\",\n  \"club\": \"Real Madrid\",\n  \"fee\": \"$100 million\",\n  \"contract\": \"5-year deal\"\n}"
    # x = generate_from_prompt(content=content)
    # b =1
    asyncio.run(refresh_bluffs())
