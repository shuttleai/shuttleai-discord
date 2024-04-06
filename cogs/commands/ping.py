from discord.ext import commands
from discord import app_commands
import discord
import os
import psutil

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping_command(self, interaction):
     try:
        latency = round(self.bot.latency * 1000) 
        shard_id = interaction.guild.shard_id if interaction.guild else 0
        
        process = psutil.Process(os.getpid())
        memory_info = psutil.virtual_memory()
        memory_usage = round((process.memory_info().rss / 1024 / 1024) / 1024, 2)  
        total_memory = round(memory_info.total / (1024.0 ** 3))  
        cpu_usage = process.cpu_percent(0.1)  

        guilds_in_shard = [guild for guild in self.bot.guilds if guild.shard_id == shard_id]
        servers_in_shard = len(guilds_in_shard)
        members_in_shard = sum(guild.member_count for guild in guilds_in_shard)

        total_servers = len(self.bot.guilds)
        total_members = sum(guild.member_count for guild in self.bot.guilds)

        embed = discord.Embed(title='ShuttleAI Info ✅', colour=discord.Color(0x2b2d31))
        embed.add_field(name='🏓 Latency', value=f'`{latency}ms`', inline=True)
        embed.add_field(name='🆔 Shard ID', value=f'`{shard_id}`', inline=True)
        embed.add_field(name='🧠 RAM Usage', value=f'`{memory_usage}GB/{total_memory}GB`', inline=True)
        embed.add_field(name='🔋 CPU Usage', value=f'`{cpu_usage}%`', inline=True)
        embed.add_field(name='🔗 Servers in Shard', value=f'`{servers_in_shard}`', inline=True)
        embed.add_field(name='👥 Members in Shard', value=f'`{members_in_shard}`', inline=True)
        embed.add_field(name='🌐 Total Servers', value=f'`{total_servers}`', inline=True)
        embed.add_field(name='👥 Total Members', value=f'`{total_members}`', inline=True)
        embed.add_field(name='✅ Status', value=f'`Healthy`', inline=True)
        await interaction.response.send_message(embed=embed)

     except Exception as e:
        print(e)

async def setup(bot):
    await bot.add_cog(Ping(bot))