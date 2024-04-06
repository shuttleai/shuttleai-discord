import io
import time
import orjson
import discord
from discord.ext import commands
from discord import app_commands

from utils import SHUTTLEAI_API_KEY, mongo, log

from backend.shuttle import shuttle_client


current_job = None

IMAGINE_MODEL_TO_CHOICE_MAP = {
    "`🚀 ShuttleAI Pro`": app_commands.Choice(name='🚀 ShuttleAI Pro', value='sdxl'),
    "`🌸 ShuttleAI Anime`": app_commands.Choice(name='🌸 ShuttleAI Anime', value='anything-v4'),
    "`💪 ShuttleAI Anything`": app_commands.Choice(name='💪 ShuttleAI Anything', value='deliberate'),
    "`🌅 ShuttleAI Journey`": app_commands.Choice(name='🌅 ShuttleAI Journey', value='openjourney'),
    "`🔞 ShuttleAI Nsfw`": app_commands.Choice(name='🔞 ShuttleAI Nsfw', value='dreamshaper-v8'),
    "`😊 ShuttleAI Emoji`": app_commands.Choice(name='😊 ShuttleAI Emoji', value='sdxl-emoji')
}

class Imagine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="imagine", description="Generates an image using ShuttleAI")
    @app_commands.choices(model=[IMAGINE_MODEL_TO_CHOICE_MAP[key] for key in IMAGINE_MODEL_TO_CHOICE_MAP])
    async def imagine(self, interaction, prompt: str, model: app_commands.Choice[str]):
        response = await self._imagine(interaction, prompt, model)
        return response
    
    async def _imagine(self, interaction, prompt, model):
        count=0

        try:
            user_id = str(interaction.user.id)

            is_premium = False
            if interaction.guild:
                try:
                    async for entitlement in self.bot.entitlements(guild=interaction.guild, exclude_ended=True):
                            is_premium = True
                except Exception as e:
                    log.error(f"An error occurred: {e}")
                    is_premium = False

            a = await mongo.is_user_in_imggendb(user_id)
            if a is False:
                await mongo.add_user_to_imggendb(user_id)

            if not is_premium:
               count: int = await mongo.increment_user_imggen(user_id) or 0
            if count > 10 and not is_premium:
                embed = discord.Embed(
                    description="You have reached your daily limit of 10 image generations. Please upgrade to premium for unlimited image generations.",
                    color=discord.Color(0x2b2d31)
                )
                await interaction.response.send_message(embed=embed)
                return
            
            await interaction.response.defer()

            # original_prompt = prompt

            async with self.bot.session.post("https://api.shuttleai.app/v1/moderations", data=orjson.dumps({'model': 'text-moderation-latest', 'input': prompt}).decode(), headers={'Authorization': f'Bearer {SHUTTLEAI_API_KEY}', 'Content-Type': 'application/json'}) as response:
                json_output = await response.json()
            output = json_output["results"][0]

            user_id = interaction.user.id

            if output["categories"]["sexual"] and not interaction.channel.is_nsfw():
                embed = discord.Embed(
                    title="No NSFW",
                    description="NSFW content is only allowed in NSFW channels.",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                return

            if output["categories"]["sexual/minors"]:
                embed = discord.Embed(
                    title="No NSFW image is allowed of lolis or minors.",
                    description="If you continue, your actions will be reported.",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                return
            
            start_time = time.time()
        
            embed = discord.Embed(
                color = discord.Color(0x2b2d31)
            )
            embed.set_image(url="https://cdn.shuttleai.app/generating.gif")  
            message = await interaction.followup.send(embed=embed)

            model_uid = model.value

            image_raw = await shuttle_client.imagine(model_uid, prompt, 'raw')
            image_data = io.BytesIO(image_raw)

            total_generation_time = time.time() - start_time

            up_emoji = bytes([0xE2, 0xAC, 0x86, 0xEF, 0xB8, 0x8F]).decode('utf-8')
            final_embed = discord.Embed(
                title="ShuttleAI Image Generation",
                color = discord.Color(0x2b2d31)
            )

            final_embed.add_field(name="\U0001F464 User", value=f"`{interaction.user.name}`", inline=True)
            final_embed.add_field(name="\U0001F916 Model", value=f"`{model.name}`", inline=True)

            final_embed.add_field(name="\U0001F552 Generation Time", value=f"`{total_generation_time:.2f} s`", inline=True)
            final_embed.add_field(name="\U0001F4AC Prompt", value=f"`{prompt}`", inline=True)

            if not is_premium:
                final_embed.set_footer(text="Daily image generations resets at 6:00 AM EST")
                final_embed.add_field(name="🚀 Daily  Generationss", value=f"```{count}/10```", inline=True)

            final_embed.set_image(url="attachment://generated_image.png")

            await interaction.followup.send(
                embed=final_embed,
                file=discord.File(image_data, filename="generated_image.png"),
                # view=self.MyView(bot=self.bot)
            )
        
            log.img(f"Generated \"{prompt}\" for {interaction.user.name}!")
        except Exception as e:
            print(f"An error occurred: {e}")
            pass

async def setup(bot):
    await bot.add_cog(Imagine(bot))