from discord.ext import commands
from discord import app_commands
import discord

from utils import add_channel

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="setup", description="Sets up the chatbot channel")
    async def setup(self, interaction, channel: discord.TextChannel): 
        if interaction.user.guild_permissions.administrator:
            mentioned_channel = channel
            add_channel(str(mentioned_channel.id))
            embed = discord.Embed(title="Setup", description="Setup Complete!", color=discord.Colour(0x2b2d31))
            message = await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="You must have administrator permissions to use this command.", color=discord.Color.red())
            message = await interaction.response.send_message(embed=embed)



async def setup(bot):
    await bot.add_cog(Setup(bot))