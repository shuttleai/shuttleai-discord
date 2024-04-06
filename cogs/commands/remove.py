from discord.ext import commands
from discord import app_commands
import discord

from utils import get_channels, remove_channel

class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="remove", description="Removes the channel from ShuttleAI")
    async def remove(self, interaction, channel: discord.TextChannel):
        if interaction.user.guild_permissions.administrator:
                mentioned_channel = channel
                remove_channel(str(mentioned_channel.id))
                embed = discord.Embed(title="Remove", description="Channel ID removed!", color=discord.Colour(0x2b2d31))
                message = await interaction.response.send_message(embed=embed)
        else:
                embed = discord.Embed(title="Error", description="You must have administrator permissions to use this command.", color=discord.Color.red())
                message = await interaction.response.send_message(embed=embed)



async def setup(bot):
    await bot.add_cog(Remove(bot))