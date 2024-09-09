import io
import time
import orjson
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os
from dotenv import load_dotenv

from utils import SHUTTLEAI_API_KEY, mongo, log

from backend.shuttle import shuttle_client

load_dotenv()

top_gg_token = os.getenv('TOP_GG_TOKEN')

def create_vote_embed():
    embed = discord.Embed(
        title="Vote for ShuttleAI",
        description="Please vote for ShuttleAI before using the `/imagine` command.\n\nPurchase premium to remove voting for this entire server using `/premium`. Voting for ShuttleAI on top.gg helps promote our discord bot.",
        color = discord.Color(0x2b2d31)
    )
    button = discord.ui.Button(label="\U0001F90D Vote Now", url="https://top.gg/bot/1100203264957497427/vote", style=discord.ButtonStyle.url)
    view = discord.ui.View()
    view.add_item(button)
    return embed, view

async def check_user_voted(user_id):
    async with aiohttp.ClientSession() as session:
        url = f"https://top.gg/api/bots/1100203264957497427/check?userId={user_id}"
        headers = {'Authorization': top_gg_token}
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data['voted']  
            else:
                return None

current_job = None

IMAGINE_MODEL_TO_CHOICE_MAP = {
    "`🪐 ShuttleAI Diffusion`": app_commands.Choice(name='🪐 Shuttle Diffusion', value='shuttle-diffusion'),
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

            if await check_user_voted(user_id):
                Voted = True
            else:
                Voted = False

            is_premium = False
            if interaction.guild:
                try:
                    async for entitlement in self.bot.entitlements(guild=interaction.guild, exclude_ended=True):
                            is_premium = True
                except Exception as e:
                    log.error(f"An error occurred: {e}")
                    is_premium = False

            if not is_premium and not Voted:
                    embed, view = create_vote_embed()
                    await interaction.response.send_message(embed=embed, view=view)

            a = await mongo.is_user_in_imggendb(user_id)
            if a is False:
                await mongo.add_user_to_imggendb(user_id)

            if not is_premium:
               count: int = await mongo.increment_user_imggen(user_id) or 0
            if count > 10 and not is_premium:
                embed = discord.Embed(
                    description="You have reached your daily limit of 10 image generations. Did you know you can generate **unlimited** images by using ShuttleAI in https://discord.gg/shuttleai",
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
            embed.set_image(url="https://media.discordapp.net/attachments/1164078703450521680/1196158940526944386/copy_4E357BFD-DAA3-4DFB-A3E9-5B6A62B98147.gif?ex=66465052&is=6644fed2&hm=1f0c7f5ab0138908dea9a83eebcaf817b819783284b80fa8696dc12500fb876a&")  
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

            button = discord.ui.Button(label="Powered by ShuttleAI", url="https://shuttleai.app/?utm_source=discord&utm_medium=imagine&utm_campaign=ShuttleAI+Discord+Bot", style=discord.ButtonStyle.url)
            view = discord.ui.View()
            view.add_item(button)

            await interaction.followup.send(
                embed=final_embed,
                view=view,
                file=discord.File(image_data, filename="generated_image.png"),
                # view=self.MyView(bot=self.bot)
            )
        
            log.img(f"Generated \"{prompt}\" for {interaction.user.name}!")
        except Exception as e:
            print(f"An error occurred: {e}")
            pass

async def setup(bot):
    await bot.add_cog(Imagine(bot))