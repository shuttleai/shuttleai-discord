from discord.ext import commands
from discord import app_commands
import discord

class HelpDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="/setup", description="Sets up the chatbot channel"),
            discord.SelectOption(label="/remove", description="Removes the channel from ShuttleAI"),
            discord.SelectOption(label="/reset", description="Resets chat history"),
            discord.SelectOption(label="/imagine", description="Generates an image"),
            discord.SelectOption(label="/settings", description="Configures the bot"),
            discord.SelectOption(label="/personality", description="Sets a custom personality")
        ]
        super().__init__(placeholder="Choose a command...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        command_info = {
            "/setup": "Run `/setup` in the channel you want to use ShuttleAI in. Any message sent in that channel will be processed by ShuttleAI. Run `/remove` to remove the channel.",
            "/remove": "Run `/remove` in the channel you want to remove ShuttleAI from processing messages in.",
            "/reset": "Run `/reset` to reset your conversation history with ShuttleAI.",
            "/imagine": "Run `/imagine` to generate an image. You can also use `/imagine-special` for premium users.",
            "/settings": "Run `/settings` to configure the bot's personality, tts, and model.",
            "/personality": "Run `/personality` to set a custom personality. This command is only available for ShuttleAI Premium users."
        }
        selected_command = self.values[0]
        embed = discord.Embed(title=f"Infomation for `{selected_command}`", description=command_info[selected_command], color=discord.Color(0x2b2d31))
        await interaction.response.edit_message(embed=embed)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(HelpDropdown())

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="help", description="Provides bot commands info")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="ShuttleAI Commands Infomation", description="**View ShuttleAI's command infomations using the dropdown menu below.\n\nShuttleAI's Server: [ShuttleAI](https://discord.gg/shuttleai)**", color=discord.Color(0x2b2d31))
        view = HelpView()
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))