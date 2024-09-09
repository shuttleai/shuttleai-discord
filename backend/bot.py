import os
import sys
import aiocron
import asyncio
import wavelink

import discord
from discord.ext import commands

import hypercorn.asyncio
from flask import Flask, jsonify

from aiohttp import ClientSession
from utils import log, mongo, STREAM_NAME, STREAM_URL

class DiscordBot:
    def __init__(self, BOT_TOKEN):
        self.BOT_TOKEN = BOT_TOKEN
        intents = discord.Intents.all()
        intents.members = False
        self.client = commands.AutoShardedBot(
            command_prefix=".",
            help_command=None,
            intents=intents,
            )
        self.client.owner_ids = [206162910848745472, 1066613998000291900] # xtristan, thoth
        self.flask_app = Flask(__name__)
        self.setup()

        self.shutting_down = False

    async def load_cogs(self):
        cog_dirs = self._get_cog_dirs('./cogs')
        for directory in cog_dirs:
            await self._load_cogs_from_dir(directory)

    def _get_cog_dirs(self, base_dir):
        cog_dirs = [root for root, _, files in os.walk(base_dir) if any(file.endswith('.py') for file in files)]
        return cog_dirs

    async def _load_cogs_from_dir(self, dir_path):
        for filename in os.listdir(dir_path):
            if filename.endswith('.py') and filename != '__init__.py':
                cog_path = os.path.join(dir_path, filename).replace('/', '.').replace('\\', '.').replace('..', '')[:-3]
                try:
                    await self.client.load_extension(cog_path)
                    log.cog(f"Loaded {filename}.")
                except Exception as e:
                    log.error(f"Failed to load extension {filename}: {e}")
    
    async def run_bot(self):
        async with self.client:
            try:
                await self.client.start(self.BOT_TOKEN)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                log.error(f"-> {e}")
            finally:
                await self.shutdown_bot()

    async def shutdown_bot(self):
        if not self.shutting_down:
            self.shutting_down = True
            log.system("Shutting down...")
            await self.client.close()
            sys.exit()

    def setup(self):
        
        @self.client.event
        async def setup_hook():
            nodes = [wavelink.Node(uri="https://music.shuttleai.app", password="Shuttle")]
            log.wavelink(f"Connecting to ShuttleAI Wavelink nodes...")
            try:
                await wavelink.Pool.connect(nodes=nodes, client=self.client, cache_capacity=None)
            except Exception as e:
                log.error(f"Failed to connect to wavelink: {e}")

            # TODO: Replace aiocron with something more appropriate 
            clear_imggens_cron = aiocron.crontab('0 11 * * *', func=mongo.clear_imgggens, start=True, loop=asyncio.get_event_loop()) # 11 AM UTC, 6 AM EST

        @self.client.event
        async def on_ready():
            try:
                await self.client.change_presence(activity=discord.Streaming(name=STREAM_NAME, url=STREAM_URL))
            except Exception as e:
                log.error(f"Failed to set streaming status: {e}, falling back to custom status.")
                await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, name="Custom ShuttleAI Status", state="https://shuttleai.app"))

            log.success(f"Logged in as {self.client.user}")

            await self.load_cogs()
            await self.client.tree.sync()
            self.client.cog

        @self.client.event
        async def on_wavelink_node_ready(payload: wavelink.NodeReadyEventPayload) -> None:
            log.wavelink(f"ShuttleAI Wavelink node is ready.")

        @self.flask_app.route('/servers', methods=['GET'])
        def get_servers():
            guilds = [{'id': str(guild.id), 'name': guild.name} for guild in self.client.guilds]
            return jsonify(guilds)
        

    async def start_flask_server(self):
        config = hypercorn.config.Config.from_mapping(
            bind=["0.0.0.0:1112"],
            loglevel="ERROR"
        )
        try:
            await hypercorn.asyncio.serve(self.flask_app, config)
        except Exception as e:
            log.error(f"Failed to start flask server: {e}")
        finally:
            await self.shutdown_bot()

    async def start(self):
        async with ClientSession() as session:
            self.client.session = session
            os.system('cls' if os.name == 'nt' else 'clear')
            log.system("Starting ShuttleAI...")
            await asyncio.gather(
                self.run_bot(),
                self.start_flask_server()
            )