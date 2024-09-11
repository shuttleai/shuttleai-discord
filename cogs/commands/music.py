from discord.ext import commands
from discord import app_commands
import discord
import requests
import urllib
import orjson
import random
from typing import cast
from discord.ui import Button, View
from utils import SHUTTLEAI_API_KEY
import asyncio
import wavelink


class PaginatedEmbed:
    def __init__(self, interaction, pages, title, author, artist, thumbnail_url, source_url):
        self.interaction = interaction
        self.pages = pages
        self.title = title
        self.author = author
        self.artist = artist
        self.thumbnail_url = thumbnail_url
        self.source_url = source_url
        self.current_page = 0
        self.message = None

    def get_embed(self):
        embed = discord.Embed(title=self.title, description=self.pages[self.current_page])
        embed.set_author(name=self.author, icon_url=self.artist.artwork)
        embed.set_thumbnail(url=self.thumbnail_url)
        embed.set_footer(text=f"Page {self.current_page + 1}/{len(self.pages)}  |  Requested by @{self.interaction.user.name}")
        return embed

    async def update_embed(self, interaction):
        await self.message.edit(embed=self.get_embed(), view=self.create_view())
        await interaction.response.edit_message(embed=self.get_embed(), view=self.create_view())

    def create_view(self):
        view = View()
        previous_button = Button(style=discord.ButtonStyle.primary, label='Previous')
        next_button = Button(style=discord.ButtonStyle.primary, label='Next')
        async def previous_callback(interaction):
            self.current_page = (self.current_page - 1) % len(self.pages)
            await self.update_embed(interaction)
        async def next_callback(interaction):
            self.current_page = (self.current_page + 1) % len(self.pages)
            await self.update_embed(interaction)
        previous_button.callback = previous_callback
        next_button.callback = next_callback
        view.add_item(previous_button)
        view.add_item(next_button)
        return view

    async def send(self):
        view = self.create_view()
        self.message = await self.interaction.followup.send(embed=self.get_embed(), view=view)

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_group = app_commands.Group(name="music", description="Music management commands")
        self.track_started = False


        @self.bot.event
        async def on_wavelink_track_start(payload: wavelink.TrackStartEventPayload) -> None:
            player: wavelink.Player | None = payload.player
            original: wavelink.Playable | None = payload.original
            track: wavelink.Playable = payload.track
            embed: discord.Embed = discord.Embed(title="Now Playing")
            embed.description = f"**{track.title}** by `{track.author}`"
            if track.artwork:
                embed.set_image(url=track.artwork)
            if original and original.recommended:
                embed.description += f"\n\n`This track was recommended via {track.source}`"
            if track.album.name:
                embed.add_field(name="Album", value=track.album.name)
            await player.home.send(embed=embed)
            self.track_started = True

        @self.bot.event
        async def on_wavelink_track_end(payload: wavelink.TrackEndEventPayload) -> None:
            player: wavelink.Player | None = payload.player
            if not player.queue:
                self.track_started = False
                await asyncio.sleep(30)
                if not self.track_started:
                    await player.disconnect()

# Commands
    # STATS
    @app_commands.command(name="stats", description="Shows global stats of how many people are listening to music.")
    async def stats(self, interaction: discord.Interaction):
        total_listeners = 0
        for guild in self.bot.guilds:
            player: wavelink.Player = guild.voice_client
            if player and player.playing:
                voice_channel = player.channel
                listeners = sum(1 for member in voice_channel.members if not member.bot and not member.voice.deaf and not member.voice.self_deaf)
                total_listeners += listeners
        embed = discord.Embed(description=f"🌐 There are **{total_listeners}** people listening to music using ShuttleAI globally.", color=discord.Color(0x2b2d31))
        await interaction.response.send_message(embed=embed)
    # SKIP
    @app_commands.command(name="skip", description="Skip the currently playing track.")
    async def skip(self, interaction: discord.Interaction):
        if interaction.guild.voice_client is None:
            embed = discord.Embed(description="Not connected to a voice channel.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        player: wavelink.Player = interaction.guild.voice_client
        if not player.queue and not player.playing:
            embed = discord.Embed(description="No track is currently playing or in the queue.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        await player.stop()
        embed = discord.Embed(description="Skipped the currently playing track.", color=discord.Color(0x2b2d31))
        await interaction.response.send_message(embed=embed)
    # AUTO
    @app_commands.command(name="auto", description="Auto plays random recommended tracks.")
    async def auto(self, interaction: discord.Interaction):
        if interaction.guild.voice_client is None:
            embed = discord.Embed(description="Not connected to a voice channel.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        player: wavelink.Player = interaction.guild.voice_client
        tracks = await wavelink.Playable.search('random', source=wavelink.TrackSource.SoundCloud)
        if not tracks:
            embed = discord.Embed(description="No tracks were found.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        random_track = random.choice(tracks)
        player.queue.put(random_track)
        if not player.playing:
            player.autoplay = wavelink.AutoPlayMode.enabled
            await player.play(player.auto_queue.get(), replace=True, start=0, volume=33)
            player.autoplay = wavelink.AutoPlayMode.enabled
            embed = discord.Embed(description=f"Playing random track: `{random_track.title}` by `{random_track.author}`.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(description=f"Added random track: `{random_track.title}` by `{random_track.author}` to the queue.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
    # NOW PLAYING
    @app_commands.command(name="nowplaying", description="Gets the current track")
    async def now_playing(self, interaction: discord.Interaction):
        player: wavelink.Player
        player = cast(wavelink.Player, interaction.guild.voice_client)
        if player is None:
            voice_channel, player = await self._connect_to_voice_channel(interaction)
        else:
            voice_channel = player.channel
        if not voice_channel or interaction.guild.voice_client is None:
            embed = discord.Embed(description="Not connected to a voice channel.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        if not player.playing:
            embed = discord.Embed(description="No track is currently playing.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        current_track = player.current.title
        current_artist = player.current.author
        position = str(player.position)
        current_length = str(player.current.length)
        position_formatted = f"{int(position) // 60000}:{(int(position) // 1000) % 60:02d}"
        current_length_formatted = f"{int(current_length) // 60000}:{(int(current_length) // 1000) % 60:02d}"
        embed = discord.Embed(description=f"Currently playing [{current_track}]({player.current.uri}) by `{current_artist}`.\n`{position_formatted}/{current_length_formatted}`", color=discord.Color(0x2b2d31))
        await interaction.response.send_message(embed=embed)
    # PLAY
    @app_commands.command(name="play", description="Play a song in a voice channel.")
    @app_commands.describe(query="The song you wish to play.")
    async def play(self, interaction: discord.Interaction, query: str = None):
        # a = await is_guild_music(str(interaction.guild.id))
        # if a is False:
        #     embed = discord.Embed(description="An owner or admin has disabled Music, enable on ShuttleAI dashboard to play music.", color=discord.Color(0x2b2d31))
        #     await interaction.response.send_message(embed=embed)
        #     return
        if "youtube.com" in query or "youtu.be" in query:
                embed = discord.Embed(description="Playing music from youtube is not allowed.", color=discord.Color(0x2b2d31))
                await interaction.response.send_message(embed=embed)
                return
        if query is None:
            if interaction.guild.voice_client is None:
                embed = discord.Embed(description="Not connected to a voice channel.", color=discord.Color(0x2b2d31))
                await interaction.response.send_message(embed=embed)
                return
            if interaction.guild.voice_client.paused:
                await interaction.guild.voice_client.pause(False)
                embed = discord.Embed(description="Resumed the current track.", color=discord.Color(0x2b2d31))
                await interaction.response.send_message(embed=embed)
                return
            else:
                embed = discord.Embed(description="No song to resume, try entering a `query`.", color=discord.Color(0x2b2d31))
                await interaction.response.send_message(embed=embed)
                return
        player: wavelink.Player
        player = cast(wavelink.Player, interaction.guild.voice_client)
        if player is None:
            voice_channel, player = await self._connect_to_voice_channel(interaction)
        else:
            voice_channel = player.channel
        if not voice_channel:
            return
        if not hasattr(player, "home"):
            player.home = interaction.user.voice.channel
        elif player.home != interaction.user.voice.channel:
            embed = discord.Embed(description=f"You can only play songs in {player.home.mention}, as the player has already started there.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        tracks = await wavelink.Playable.search(f'{query}', source=wavelink.TrackSource.SoundCloud)
        if not tracks:
            embed = discord.Embed(description="No tracks were found with that query.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
        try:
            track: wavelink.Playable = tracks[0]
            player.queue.put(track)
            if not player.playing:
                await player.play(player.queue.get(), replace=True, start=0, volume=33)
                player.autoplay = wavelink.AutoPlayMode.enabled
                embed = discord.Embed(description=f"Playing `{track.title}` by `{track.author}`.", color=discord.Color(0x2b2d31))
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(description=f"Added `{track.title}` to the queue.", color=discord.Color(0x2b2d31))
                await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            pass
    # PAUSE
    @app_commands.command(name="pause", description="Pause the currently playing track.")
    async def pause(self, interaction: discord.Interaction):
        if interaction.guild.voice_client is None:
            embed = discord.Embed(description="Not connected to a voice channel.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        if not interaction.guild.voice_client.playing:
            embed = discord.Embed(description="No track is currently playing.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        await interaction.guild.voice_client.pause(True)
        embed = discord.Embed(description="Paused the currently playing track.", color=discord.Color(0x2b2d31))
        await interaction.response.send_message(embed=embed)
    # LYRICS
    @app_commands.command(name="lyrics", description="Get the lyrics of the currently playing track.")
    @app_commands.describe(song="The Song to get Lyrics from")
    async def lyrics(self, interaction: discord.Interaction, song: str = None):
        if song is None:
            if interaction.guild.voice_client is None:
                embed = discord.Embed(description="Not connected to a voice channel.", color=discord.Color(0x2b2d31))
                await interaction.response.send_message(embed=embed)
                return
            if not interaction.guild.voice_client.playing:
                embed = discord.Embed(description="No track is currently playing.", color=discord.Color(0x2b2d31))
                await interaction.response.send_message(embed=embed)
                return
            player: wavelink.Player = interaction.guild.voice_client
            song = f'{player.current.title}'
        embed = discord.Embed(description=f"Fetching lyrics of `{song}` for `@{interaction.user.name}`. Please wait.", color=discord.Color(0x2b2d31))
        await interaction.response.send_message(embed=embed)
        song = urllib.parse.quote(song)
        r = requests.get(f"https://some-random-api.com/lyrics?title={song}")
        if r.json().get("error"):
            embed = discord.Embed(description="No lyrics found for that song.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        lyrics = r.json().get("lyrics")
        title = r.json().get("title")
        author = r.json().get("author")
        thumbnail = r.json().get("thumbnail").get("genius")
        if lyrics:
            if len(lyrics) > 1000:
                pages = []
                chunks = [lyrics[i:i+1000] for i in range(0, len(lyrics), 1000)]
                for chunk in chunks:
                    try:
                        pages.append(chunk)
                    except:
                        pass
            else:
                pages = [lyrics]
            paginated_embed = PaginatedEmbed(interaction, pages, title, author, player.current.artist, thumbnail, None)
            await paginated_embed.send()
            return True
    # SUMMARY
    @app_commands.command(name="summary", description="Get an AI generated summary of the currently playing track.")
    async def summary(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.guild.voice_client is None:
            embed = discord.Embed(description="Not connected to a voice channel.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        if not interaction.guild.voice_client.playing:
            embed = discord.Embed(description="No track is currently playing.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        player: wavelink.Player = interaction.guild.voice_client
        title = player.current.title
        song = urllib.parse.quote(title)
        r = requests.get(f"https://some-random-api.com/lyrics?title={song}")
        author = player.current.author
        lyrics = r.json().get("lyrics")
        title = r.json().get("title")
        author = r.json().get("author")
        summary = "AI Summary could not be generated."
        summary = await self.ask_ai_to_summarize_song(lyrics, author, title)
        embed = discord.Embed(description=f"Summary of `{title}` by `{author}`: {summary}", color=discord.Color(0x2b2d31))
        await interaction.followup.send(embed=embed)
    # VOLUME
    @app_commands.command(name="volume", description="Adjust the volume of the player.")
    @app_commands.describe(volume="The volume level (0-100).")
    async def volume(self, interaction: discord.Interaction, volume: int = None):
        if volume is None:
            if interaction.guild.voice_client is None:
                embed = discord.Embed(description="Not connected to a voice channel.", color=discord.Color(0x2b2d31))
                await interaction.response.send_message(embed=embed)
                return
            if interaction.guild.voice_client.playing:
                embed = discord.Embed(description=f"Volume is currently set to `{interaction.guild.voice_client.volume}`.", color=discord.Color(0x2b2d31))
                await interaction.response.send_message(embed=embed)
                return
            else:
                embed = discord.Embed(description=f"Volume is currently set to `{interaction.guild.voice_client.volume}`.", color=discord.Color(0x2b2d31))
                await interaction.response.send_message(embed=embed)
                return
        if volume < 0 or volume > 100:
            embed = discord.Embed(description="Volume must be between 0 and 100.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.set_volume(volume)
        embed = discord.Embed(description=f"Volume set to `{volume}`.", color=discord.Color(0x2b2d31))
        await interaction.response.send_message(embed=embed)
    # QUEUE
    @app_commands.command(name="queue", description="Show the list of tracks in the queue.")
    async def queue(self, interaction: discord.Interaction):
        player = interaction.guild.voice_client
        if not player.queue:
            embed = discord.Embed(description="The queue is currently empty.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        queue_embed = discord.Embed(title="Music Queue", description="")
        for i, track in enumerate(player.queue, start=1):
            queue_embed.description += f"{i}. [{track.title}]({track.uri}) by {track.author}\n"
        await interaction.response.send_message(embed=queue_embed)
    # FILTERS
    @app_commands.command(name="nightcore", description="Toggle the nightcore filter for the currently playing track.")
    async def nightcore(self, interaction: discord.Interaction):
        player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player.playing:
            embed = discord.Embed(description="No track is currently playing.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        filters: wavelink.Filters = player.filters
        if filters.timescale.get("pitch") == 1.2 and filters.timescale.get('speed') == 1.2 and filters.timescale.get('rate') == 1:
            filters.timescale.set(pitch=1, speed=1, rate=1)
            embed = discord.Embed(description="Disabled the nightcore filter for the currently playing track.", color=discord.Color(0x2b2d31))
        else:
            filters.timescale.set(pitch=1.2, speed=1.2, rate=1)
            embed = discord.Embed(description="Enabled the nightcore filter for the currently playing track.", color=discord.Color(0x2b2d31))
        await player.set_filters(filters)
        await interaction.response.send_message(embed=embed)
    @app_commands.command(name="vaporwave", description="Toggle the vaporwave filter for the currently playing track.")
    async def vaporwave(self, interaction: discord.Interaction):
        player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player.playing:
            embed = discord.Embed(description="No track is currently playing.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        filters: wavelink.Filters = player.filters
        if filters.timescale.get('pitch') == 0.5 and filters.timescale.get('speed') == 0.5 and filters.timescale.get('rate') == 1:
            filters.timescale.set(pitch=1, speed=1, rate=1)
            embed = discord.Embed(description="Disabled the vaporwave filter for the currently playing track.", color=discord.Color(0x2b2d31))
        else:
            filters.timescale.set(pitch=0.5, speed=0.5, rate=1)
            embed = discord.Embed(description="Enabled the vaporwave filter for the currently playing track.", color=discord.Color(0x2b2d31))
        await player.set_filters(filters)
        await interaction.response.send_message(embed=embed)
    @app_commands.command(name="rotation", description="Toggle the rotation filter for the currently playing track.")
    async def rotation(self, interaction: discord.Interaction):
        player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player.playing:
            embed = discord.Embed(description="No track is currently playing.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        filters: wavelink.Filters = player.filters
        if filters.rotation.get('rotation_hz') != 0.0:
            filters.rotation.set(rotation_hz=0.2)
            embed = discord.Embed(description="Enabled the rotation filter for the currently playing track.", color=discord.Color(0x2b2d31))
        else:
            filters.rotation.set(rotation_hz=0.0)
            embed = discord.Embed(description="Disabled the rotation filter for the currently playing track.", color=discord.Color(0x2b2d31))
        await player.set_filters(filters)
        await interaction.response.send_message(embed=embed)
    @app_commands.command(name="bassboost", description="Toggle the bassboost filter for the currently playing track.")
    async def bassboost(self, interaction: discord.Interaction):
        player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player.playing:
            embed = discord.Embed(description="No track is currently playing.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return
        filters: wavelink.Filters = player.filters
        if filters.equalizer.payload[0].get('gain') != 0.0:
            embed = discord.Embed(description="Disabled the bassboost filter for the currently playing track.", color=discord.Color(0x2b2d31))
        else:
            filters.equalizer.set(bands=[{"band": 0, "gain": 0.25}, {"band": 1, "gain": 0.25}, {"band": 2, "gain": 0.25}])
            embed = discord.Embed(description="Enabled the bassboost filter for the currently playing track.", color=discord.Color(0x2b2d31))
        await player.set_filters(filters)
        await interaction.response.send_message(embed=embed)

# Helpers
    async def _connect_to_voice_channel(self, interaction):
        if interaction.user.voice is None:
            embed = discord.Embed(description="You must be connected to a voice channel.", color=discord.Color(0x2b2d31))
            await interaction.response.send_message(embed=embed)
            return None, None
        voice_channel = interaction.user.voice.channel
        if voice_channel.guild.voice_client is None:
            player: wavelink.Player
            player = await voice_channel.connect(cls=wavelink.Player)
        else:
            player: wavelink.Player
            player = await voice_channel.guild.voice_client.move_to(voice_channel, cls=wavelink.Player)
        return voice_channel, player
    

    async def ask_ai_to_summarize_song(self, lyrics, author, title):
        async with self.bot.session.post(
            "https://api.shuttleai.com/v1/chat/completions",
            data=orjson.dumps({
                'model': "shuttle-2.5-mini",
                'messages': [
                    {"role": "system", "content": "You are an AI Music DJ/Host bot. You will summarize and give information on the songs provided. You will be provided lyircs, artist, and title. Please summarize the song and give information on the song."},
                    {"role": "user", "content": f"Song to summarize -> Lyrics: {lyrics} Artist: {author} Title: {title}"}
                ],
                'stream': False,
                'internet': False
            }).decode(),
            headers={'Authorization': f'Bearer {SHUTTLEAI_API_KEY}', 'Content-Type': 'application/json'}
        ) as response:
            response.raise_for_status()
            return (await response.json(loads=orjson.loads, encoding="utf-8"))["choices"][0]["message"]["content"]
        # a = "No." # TODO: Fix ai summary
        # a = ask_sync(f"You are an AI Music DJ/Host bot. You will summarize and give information on the songs provided. You will be provided lyircs, artist, and title. Please summarize the song and give information on the song. Lyrics: {lyrics} Artist: {author} Title: {title}", [], None, "gemini-pro")
        # return a

async def setup(bot):
    if 'music' in bot.all_commands:
        bot.remove_command('music')
    music_cog = MusicCog(bot)
    music_cog.music_group.add_command(music_cog.play)
    music_cog.music_group.add_command(music_cog.pause)
    music_cog.music_group.add_command(music_cog.lyrics)
    music_cog.music_group.add_command(music_cog.now_playing)
    music_cog.music_group.add_command(music_cog.summary)
    music_cog.music_group.add_command(music_cog.volume)
    music_cog.music_group.add_command(music_cog.queue)
    music_cog.music_group.add_command(music_cog.auto)
    music_cog.music_group.add_command(music_cog.skip)
    music_cog.music_group.add_command(music_cog.stats)
    music_cog.music_group.add_command(music_cog.nightcore)
    music_cog.music_group.add_command(music_cog.vaporwave)
    music_cog.music_group.add_command(music_cog.rotation)
    music_cog.music_group.add_command(music_cog.bassboost)

    # await bot.add_cog(music_cog)
    bot.tree.add_command(music_cog.music_group)