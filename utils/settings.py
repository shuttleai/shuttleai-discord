"""
This is a settings manager module.

We will handle:
- UserSettings (managed via memory)
- GuildSettings (managed by mongodb database)
"""

from dataclasses import dataclass
from typing import Optional
from utils import mongo

"""
# UserSettings

Here we need to create a user settings manager which will load and hanle user settings.

User settings will consist of:
- model: str
- personality: str
- tts: bool
"""
class UserSettings:
    def __init__(self, discord_id: str, model: str, personality: str, tts: bool):
        self.discord_id = discord_id
        self.model = model
        self.personality = personality
        self.tts = tts

    def __repr__(self):
        return f"<UserSettings user_id={self.user_id} model={self.model} personality={self.personality} tts={self.tts}>"
    
    def __str__(self):
        return f"UserSettings for user_id={self.user_id}:\n\tmodel={self.model}\n\tpersonality={self.personality}\n\ttts={self.tts}"
    
    def to_dict(self):
        return {self.discord_id: {"model": self.model, "personality": self.personality, "tts": self.tts}}
    
    def update(self, model: str = None, personality: str = None, tts: bool = None):
        if model:
            self.model = model
        if personality:
            self.personality = personality
        if tts:
            self.tts = tts
        return self

class UserSettingsManger:
    def __init__(self):
        self.user_settings = {}

    def __repr__(self):
        return f"<UserSettingsManager user_settings={self.user_settings}>"
    
    def __str__(self):
        return f"UserSettingsManager with {len(self.user_settings)} user settings."
    
    def add_user_settings(self, user_settings: UserSettings):
        self.user_settings.update(user_settings.to_dict())
        return self
    
    def get_or_create_user_settings(self, discord_id: str) -> Optional[dict]:
        if discord_id in self.user_settings:
            return self.user_settings[discord_id]
        else:
            user_settings = UserSettings(discord_id, "shuttle-turbo", "ShuttleAI", False)
            self.add_user_settings(user_settings)
            return user_settings.to_dict()[discord_id]


"""
# GuildSettings

Here we need to create a guild settings manager which will load and hanle guild settings.

Guild settings will consist of:
- owner: str
- tone: str
- personality: str
- enableImageGen: bool
- enableMusic: bool

Guild settings are special in a way because although the settings are for Guilds and not users, they are set By an admin or owner of a Guild in the bot dashboard.

Also note that guild settings are stored in a mongodb database. We will utilize our MongoManager class to handle this.
"""
@dataclass
class GuildSettings:
    guild_id: str
    owner: str
    tone: str
    personality: str
    enableImageGen: bool
    enableMusicGen: bool

    def __repr__(self):
        return f"<GuildSettings guild_id={self.guild_id}>"

    def to_dict(self):
        return self.__dict__

class GuildSettingsManager:
    async def get_or_create_guild_settings(self, guild_id: str) -> Optional[GuildSettings]:
        settings_data = await mongo.get_or_create_guild_settings(guild_id)
        if settings_data:
            return GuildSettings(**settings_data)
        return None

    async def update_guild_settings(self, guild_id: str, **kwargs):
        await mongo.update_guild_settings(guild_id, **kwargs)

# Initialize Settings
user_settings_manager = UserSettingsManger()
guild_settings_manager = GuildSettingsManager()