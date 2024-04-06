from youtube_transcript_api import YouTubeTranscriptApi
from discord.ext import commands
from discord import app_commands, Embed
import discord
import aiohttp
import json

from utils import SHUTTLEAI_API_KEY

def load_cache():
    try:
        with open('summary.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open('summary.json', 'w') as file:
            json.dump({}, file, indent=4)
        return {}
    
def save_cache(cache):
    existing_cache = load_cache()
    existing_cache.update(cache)
    with open('summary.json', 'w') as file:
        json.dump(existing_cache, file, indent=4)
    print("Saving cache")

class summary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="summary", description="Generate a summary of a YouTube video with ShuttleAI")
    @app_commands.describe(video_url="YouTube video URL")
    async def youtube_summary(self, interaction: discord.Interaction, video_url: str):
        if "youtu.be" in video_url:
            videoId = video_url.split("/")[-1]
            video_thumbnail = f"https://img.youtube.com/vi/{videoId}/maxresdefault.jpg"
        else:
            videoId = video_url.split("v=")[1]
            video_thumbnail = f"https://img.youtube.com/vi/{videoId}/maxresdefault.jpg"
        if '?' in videoId:
            videoId = videoId.split("?")[0]
        if '&' in videoId:
            videoId = videoId.split("&")[0]

        print(videoId)

        cache = load_cache()

        if cache is not None and videoId in cache:
            await interaction.response.defer()
            ai_content = cache[videoId]
            if len(ai_content) > 2000:
                for i in range(0, len(ai_content), 2000):
                    embed = Embed(description=ai_content[i:i + 2000], color=discord.Color(0x2b2d31))
                    embed.set_author(name="ShuttleAI YouTube Summarizer")
                    embed.set_thumbnail(url=video_thumbnail)
                    # embed.set_footer(text=video_title)
                    await interaction.followup.send(embed=embed)
            else:
                embed = Embed(description=ai_content, color=discord.Color(0x2b2d31))
                embed.set_author(name="ShuttleAI YouTube Summarizer")
                embed.set_thumbnail(url=video_thumbnail)
                # embed.set_footer(text=video_title)
                await interaction.followup.send(embed=embed)
            return
        shuttle_url = 'https://api.shuttleai.app/v1/chat/completions'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {SHUTTLEAI_API_KEY}"
        }

        await interaction.response.defer()

        try:
            summarize_response = YouTubeTranscriptApi.get_transcript(videoId)

            model = 'gemini-pro'
            if len(summarize_response) > 1000:
                model = 'mistral-medium'

            deepinfra_data = {
                'model': model,
                'messages': [
                    {
                        "role": "system",
                        "content": "You are a youtube video summarizer bot. Summarize all of the data given in a format with bullet points, keep it long and concize and in points. Do not use over 1900 characters."
                    },
                    {
                        "role": "user",
                        "content": f"Summarize: {summarize_response}."
                    },
                ],
                'stream': False
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(shuttle_url, headers=headers, json=deepinfra_data) as response:
                    deepinfra_response = await response.json()
                    print(deepinfra_response)
                    print(response.text)

            ai_content = deepinfra_response.get('choices', [{}])[0].get('message', {}).get('content', '')

            if len(ai_content) > 2000:
                for i in range(0, len(ai_content), 2000):
                    embed = Embed(description=ai_content[i:i + 2000], color=discord.Color(0x2b2d31))
                    embed.set_author(name="ShuttleAI YouTube Summarizer")
                    embed.set_thumbnail(url=video_thumbnail)
                    # embed.set_footer(text=video_title)
                    await interaction.followup.send(embed=embed)
            else:
                embed = Embed(description=ai_content, color=discord.Color(0x2b2d31))
                embed.set_author(name="ShuttleAI YouTube Summarizer")
                embed.set_thumbnail(url=video_thumbnail)
                # embed.set_footer(text=video_title)
                await interaction.followup.send(embed=embed)
            save_cache({videoId: ai_content})
            print("Saved to cache")
        except Exception as e:
            print(e)
            embed = Embed(description="❌ Could not generate summary for the YouTube video provided! ", color=discord.Color.red())
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(summary(bot))