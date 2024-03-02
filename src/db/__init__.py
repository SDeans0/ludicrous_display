import asyncio
import os
from typing import Optional

import motor.motor_asyncio
from beanie import Document, Indexed, init_beanie
from pydantic import BaseModel

from db.football import Match, Transfer
from db.gpt import Bluff


def create_connstring(include_replicaset: bool = False):
    connection_params = ["mongodb+srv://", os.environ.get("MONGODB_USER"), ":", os.environ.get("MONGODB_PASSWORD"), "@", os.environ.get("MONGODB_HOST"), "/", os.environ.get("MONGODB_DATABASE"), "?authSource=admin"]
    if include_replicaset:
        connection_params.append("&replicaSet=")
        connection_params.append(os.environ.get("MONGODB_REPLICASET"))
    connection_params.append("&tls=true")
    return "".join(connection_params)


def create_client():
    conn = create_connstring()
    return motor.motor_asyncio.AsyncIOMotorClient(conn)


def get_db():
    client = create_client()
    return client[os.environ.get("MONGODB_DATABASE")]


async def start_beanie_session():
    db = get_db()
    await init_beanie(database=db, document_models=[Transfer, Match, Bluff])
