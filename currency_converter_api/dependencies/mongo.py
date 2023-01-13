from motor import motor_asyncio
from pymongo.errors import ConnectionFailure
from functools import wraps

from currency_converter_api.settings import MONGODB_URL
from currency_converter_api.schemas import CreateUser
from currency_converter_api.errors import MongoDbError

client = motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.db
collection_users = database.users


def mongo_operation(func):
    """
    Custom error handler for Mongo DB
    """
    @wraps(func)
    async def _mongo_operation(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ConnectionFailure as error:
            raise MongoDbError(details=str(error))
    return _mongo_operation


@mongo_operation
async def create_user(user: CreateUser) -> None:
    await collection_users.insert_one(user)


@mongo_operation
async def get_user_by_email(email: str) -> dict:
    user = await collection_users.find_one({"email": email})
    return user


@mongo_operation
async def get_user_by_api_key(api_key: str) -> dict:
    user = await collection_users.find_one({"api_key": api_key})
    return user


@mongo_operation
async def get_all_users() -> list:
    all_users = []
    cursor = await collection_users.find({})
    async for user in cursor:
        all_users.append(CreateUser(**user))
    return all_users


@mongo_operation
async def remove_user(email: str) -> None:
    await collection_users.delete_one({"email": email})


@mongo_operation
async def update_credits(api_key: str, credits_left: int) -> None:
    await collection_users.update_one(
        {"api_key": api_key},
        {'$set': {"credits_left": credits_left}}
    )
