from .log import log

from .mongodb import mongo

from .settings import user_settings_manager, guild_settings_manager
from .conversations import conversation_manager

from .chat_channels import (
    get_channels,
    add_channel, remove_channel
)

from .prompts import (
    create_shuttleai_prompt, create_chatgpt_prompt,
    create_discord_kitten_prompt, create_rude_prompt,
    create_instructions, create_instructions_for_personality
)

from .env import (
    SHUTTLEAI_API_KEY, DISCORD_BOT_TOKEN,
    STREAM_URL, STREAM_NAME,
    MONGO_URI, OWNER_IDS
)