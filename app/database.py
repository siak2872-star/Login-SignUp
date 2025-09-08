import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URL)
db = client["LoginSignUpPage"]
users_collection = db["users"]
