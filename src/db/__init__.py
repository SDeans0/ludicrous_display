import asyncio
import os
from typing import Optional

import motor.motor_asyncio
from beanie import Document, Indexed, init_beanie
from pydantic import BaseModel

from db.football import Match, Transfer
from db.gpt import Bluff


def create_connstring():
    conn = "mongodb+srv://"
    conn += os.environ.get("MONGODB_USER") + ":"
    conn += os.environ.get("MONGODB_PASSWORD") + "@"
    conn += os.environ.get("MONGODB_HOST") + "/"
    conn += os.environ.get("MONGODB_DATABASE") + "?authSource=admin&replicaSet="
    conn += os.environ.get("MONGODB_REPLICASET") + "&tls=true"
    return conn


def create_client():
    conn = create_connstring()
    return motor.motor_asyncio.AsyncIOMotorClient(conn)


def get_db():
    client = create_client()
    return client[os.environ.get("MONGODB_DATABASE")]


async def start_beanie_session():
    db = get_db()
    await init_beanie(database=db, document_models=[Transfer, Match, Bluff])

class Category(BaseModel):
    name: str
    description: str


class Product(Document):
    name: str                          # You can use normal types just like in pydantic
    description: Optional[str] = None
    price: Indexed(float)              # You can also specify that a field should correspond to an index
    category: Category                 # You can include pydantic models as well


# This is an asynchronous example, so we will access it from an async function
async def example():
    # Beanie uses Motor async client under the hood 
    client = create_client()

    # Initialize beanie with the Product document class
    await init_beanie(database=client.dev, document_models=[Product])

    chocolate = Category(name="Chocolate", description="A preparation of roasted and ground cacao seeds.")
    # Beanie documents work just like pydantic models
    tonybar = Product(name="Tony's", price=5.95, category=chocolate)
    # And can be inserted into the database
    await tonybar.insert() 

    # You can find documents with pythonic syntax
    product = await Product.find_one(Product.price < 10)

    # And update them
    await product.set({Product.name:"Gold bar"})


if __name__ == "__main__":
    asyncio.run(example())