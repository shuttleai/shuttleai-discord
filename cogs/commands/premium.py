from discord.ext import commands
from discord import app_commands
import discord

from utils import log

class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="premium", description="Shuttle Premium")
    async def premium(self, interaction):
        try:
            async for entitlement in self.bot.entitlements(guild=interaction.guild, exclude_ended=True):
                embed = discord.Embed(
                    title="Shuttle Premium :gem:",
                    description="Thank you for buying Shuttle Premium!",
                    color=discord.Colour(0xc6e7ff)
                    )
                message = await interaction.response.send_message(embed=embed)
                return
            else:
                await interaction.response.require_premium()

        except Exception as e:
            log.error(f"An error occurred: {e}")
            await interaction.response.send_message("An error occurred while checking the subscription.")

async def setup(bot):
    await bot.add_cog(Premium(bot))