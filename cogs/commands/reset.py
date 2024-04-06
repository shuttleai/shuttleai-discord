import discord
from discord.ext import commands
from discord import app_commands

from utils import conversation_manager

class Reset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reset", description="Resets chat history")
    async def reset(self, interaction):
        user_id = str(interaction.user.id)
        if user_id in conversation_manager.conversations:
            conversation_manager.clear_messages(user_id)
            # message_history[key].clear()
            embed = discord.Embed(title="Reset", description="Your conversation history has been reset.", color=discord.Colour(0x2b2d31))
            message = await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="Reset", description="You don't have any conversation history to reset.", color=discord.Colour(0x2b2d31))
            message = await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Reset(bot))