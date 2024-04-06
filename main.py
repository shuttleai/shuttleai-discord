import asyncio
from utils import DISCORD_BOT_TOKEN
from backend.bot import DiscordBot

if __name__ == "__main__":
    bot = DiscordBot(DISCORD_BOT_TOKEN)
    asyncio.run(bot.start())