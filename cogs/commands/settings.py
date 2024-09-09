import discord
from discord.ext import commands
from discord import app_commands

from utils import user_settings_manager, guild_settings_manager

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="settings", description="Personal Settings")
    async def settings_command(self, interaction):
        discord_id = str(interaction.user.id)
        guild_id = str(interaction.guild.id) if interaction.guild else None
        user_settings = user_settings_manager.get_or_create_user_settings(discord_id)
        tts_status = user_settings['tts']
        personality = user_settings['personality'] if isinstance(user_settings['personality'], str) else "Custom"
        model = user_settings['model']

        embed = discord.Embed(title="Personal Settings", description=f"**:loud_sound: TTS:** `{'Enabled' if tts_status else 'Disabled'}`\n**:brain: Personality:** `{personality}`\n**:robot: Model:** `{model}`", color=discord.Color(0x2b2d31))
        view = self.TTSView()
        await interaction.response.send_message(embed=embed, view=view)
    
    class TTSView(discord.ui.View):
        @discord.ui.button(label='TTS', style=discord.ButtonStyle.primary, row=1, emoji="🔊")
        async def toggle_tts(self, interaction: discord.Interaction, button: discord.ui.Button):
            discord_id = str(interaction.user.id)
            user_settings = user_settings_manager.get_or_create_user_settings(discord_id)
            user_settings['tts'] = not user_settings['tts']
            
            model = user_settings['model']
            embed = discord.Embed(title="Personal Settings", description=f"**:loud_sound: TTS:** `{'Enabled' if user_settings['tts'] else 'Disabled'}`\n**:brain: Personality:** `{user_settings['personality']}`\n**:robot: Model:** `{model}`", color=discord.Color(0x2b2d31))
            await interaction.response.edit_message(embed=embed)
    
        @discord.ui.button(label='Personality', style=discord.ButtonStyle.secondary, row=1, emoji="🧠")
        async def change_personality(self, interaction: discord.Interaction, button: discord.ui.Button):
            discord_id = str(interaction.user.id)
            user_settings = user_settings_manager.get_or_create_user_settings(discord_id)

            personalities = ["ShuttleAI", "ChatGPT", "Rude", "Discord Kitten"]
            current_personality = user_settings['personality']
            current_index = personalities.index(current_personality)
            next_index = (current_index + 1) % len(personalities)
            next_personality = personalities[next_index]
            user_settings['personality'] = next_personality

            model = user_settings['model']  
            embed = discord.Embed(title="Personal Settings", description=f"**:loud_sound: TTS:** `{'Enabled' if user_settings['tts'] else 'Disabled'}`\n**:brain: Personality:** `{user_settings['personality']}`\n**:robot: Model:** `{model}`", color=discord.Color(0x2b2d31))
            await interaction.response.edit_message(embed=embed)


        @discord.ui.button(label='Model', style=discord.ButtonStyle.primary, row=1, emoji="🤖")
        async def toggle_model(self, interaction: discord.Interaction, button: discord.ui.Button):
            discord_id = str(interaction.user.id)
            user_settings = user_settings_manager.get_or_create_user_settings(discord_id)

            current_model = user_settings['model']
            models = ["shuttle-2.5"]
            current_index = models.index(current_model)
            next_index = (current_index + 1) % len(models)
            next_model = models[next_index]
            user_settings['model'] = next_model

            embed = discord.Embed(
                title="Personal Settings",
                description=f"**:loud_sound: TTS:** `{'Enabled' if user_settings['tts'] else 'Disabled'}`\n**:brain: Personality:** `{user_settings['personality']}`\n**:robot: Model:** `{user_settings['model']}`",
                color=discord.Color(0x2b2d31))
            await interaction.response.edit_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Settings(bot))