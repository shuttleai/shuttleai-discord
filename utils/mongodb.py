from motor.motor_asyncio import AsyncIOMotorClient
from .env import MONGO_URI
from .log import log

class MongoDBManager:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client['shuttleai']
        self.guild_settings_collection = self.db['settings']
        self.imggen_collection = self.db['imggens']

    # IMG GENS
    async def clear_imgggens(self):
        log.system("Clearing Image Gen collections")
        await self.imggen_collection.delete_many({})

    async def is_guild_in_imggendb(self, guild_id):
        imggenobj = await self.imggen_collection.find_one({"guild_id": {"$exists": True, "$eq": str(guild_id)}})
        if imggenobj:
            return True
        else:
            return False

    async def is_user_in_imggendb(self, user_id):
        imggenobj = await self.imggen_collection.find_one({"user_id": {"$exists": True, "$eq": str(user_id)}})
        if imggenobj:
            return True
        else:
            return False

    async def get_user_in_imggendb(self, user_id):
        imggenobj = await self.imggen_collection.find_one({"user_id": str(user_id)})
        return imggenobj

    async def add_user_to_imggendb(self, user_id):
        imggenobj = await self.imggen_collection.find_one({"user_id": str(user_id)})
        if imggenobj:
            return
        else:
            await self.imggen_collection.insert_one({"user_id": str(user_id), "imageGens": 0})

    async def increment_user_imggen(self, user_id):
        imggenobj = await self.imggen_collection.find_one({"user_id": str(user_id)})
        if imggenobj:
            count = imggenobj["imageGens"]
            count += 1
            await self.imggen_collection.update_one({"user_id": str(user_id)}, {"$set": {"imageGens": count}})
            return count

    # GUILD SETTINGS
    async def _get_guild_settings(self, guild_id: str):
        return await self.guild_settings_collection.find_one({"guild_id": guild_id})
    
    async def _set_default_guild_settings(self, guild_id: str):
        default_settings = {
            "guild_id": guild_id,
            "owner": "xtristan & thoth",
            "personality": "ShuttleAI",
            "tone": "chill, fun",
            "enableImageGen": True,
            "enableMusicGen": True
        }
        await self.guild_settings_collection.insert_one(default_settings)
        return default_settings

    async def update_guild_settings(self, guild_id: str, **kwargs):
        await self.guild_settings_collection.update_one({"guild_id": guild_id}, {"$set": kwargs}, upsert=True)

    async def get_or_create_guild_settings(self, guild_id: str):
        settings = await self._get_guild_settings(guild_id)
        if not settings:
            settings = await self._set_default_guild_settings(guild_id)
        return settings

mongo = MongoDBManager()