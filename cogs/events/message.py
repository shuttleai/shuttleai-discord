import time
import orjson
import asyncio
import discord
from discord.ext import commands
from utils import log, SHUTTLEAI_API_KEY, conversation_manager, user_settings_manager, guild_settings_manager, get_channels, create_instructions_for_personality
import random
from typing import Dict, Tuple


class RateLimiter:
    def __init__(self, max_messages: int = 3, interval_seconds: int = 5, block_time: int = 120):
        self.max_messages = max_messages
        self.interval_seconds = interval_seconds
        self.block_time = block_time
        self.user_msgs: Dict[int, Tuple[int, float]] = {}
        self.reset_time = time.time() + self.interval_seconds
        self.blocked_users: Dict[int, float] = {}

    def is_rate_limited(self, user_id: int) -> bool:
        now = time.time()
        if user_id in self.blocked_users:
            if now - self.blocked_users[user_id] >= self.block_time:
                del self.blocked_users[user_id]
            else:
                return True
        if now >= self.reset_time:
            self.user_msgs = {}
            self.reset_time = now + self.interval_seconds
        msgs, last_reset = self.user_msgs.get(user_id, (0, 0))
        if msgs >= self.max_messages:
            self.blocked_users[user_id] = now
            return True
        self.user_msgs[user_id] = (msgs + 1, last_reset)
        return False


class MessageCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_response_counter = {}
        self.sent_rate_limit_embed_user_ids = set()
        self.rate_limiter = RateLimiter(max_messages=3, interval_seconds=5, block_time=180)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Initial return checks
        if message.author.bot or len(message.embeds) > 0 or message.author == self.bot.user:
            return
        if message.mention_everyone and message.webhook_id is None:
            return
        
        # Get ids as string
        discord_id = str(message.author.id)
        guild_id = str (message.guild.id) if message.guild else None
        
        if self.bot.user in message.mentions or str(message.channel.id) in get_channels() or message.channel.type == discord.ChannelType.private:

            # Check rate limits
            if self.rate_limiter.is_rate_limited(message.author.id):
                if message.author.id in self.sent_rate_limit_embed_user_ids:
                    return
                user_msgs, last_reset = self.rate_limiter.user_msgs.get(message.author.id, (0, 0))
                time_left = self.rate_limiter.block_time - (time.time() - self.rate_limiter.blocked_users[message.author.id])
                rate_limit_end = int(time.time() + time_left)
                embed = discord.Embed(
                    title="⏱ Rate Limited",
                    description=f"You can send another message <t:{rate_limit_end}:R>.",
                    color=0xFF0000
                )
                await message.channel.send(embed=embed)
                self.sent_rate_limit_embed_user_ids.add(message.author.id)
                return
            
            
            # Check settings
            user_settings = user_settings_manager.get_or_create_user_settings(discord_id)
            model = user_settings.get('model', 'shuttle-2.5')
            # TODO: Guild settings

            # Get personality
            personality = user_settings.get('personality', 'ShuttleAI')

            # Set Env Info
            guild_name = message.guild.name if message.guild else "DMs"
            guild_owner_name = await message.guild.fetch_member(message.guild.owner_id) if message.guild else "DMs"
            channel_name = message.channel.name if message.guild else "DMs"
            message_author_name = message.author._user.display_name

            # Create instructions
            instructions = create_instructions_for_personality(personality, guild_name, guild_owner_name, channel_name, message_author_name, discord_id)

            # Send warning if needed
            # if personality in ["Rude", "Discord Kitten"]:
            #     if model != "airoboros-70b":
            #         embed = discord.Embed(
            #             title="Warning",
            #             description=f"Model `airoboros-70b` is recommended to be used with **{personality}** mode.",
            #             color=discord.Color.yellow()
            #         )
            #         await message.channel.send(embed=embed)

            # Try the request
            try:
                async with message.channel.typing():
                    conversation = conversation_manager.get_or_create_conversation(discord_id)

                    # Replace bot mention from message content
                    message_content = message.content.replace(f'<@1100203264957497427>', '').replace(f'<@1219146238738436216>', '').strip()
                    conversation.add_message('user', message_content)

                    # Log request
                    log.message(f"Received message from [{message.author}]: {message_content}")

                    if not message_content:
                        responses = ["Yes??", "Hello?", "Can I help you?", "What can I do for you?", "Need something?", "What's up?", "How can I help you?", "What's on your mind"]
                        await asyncio.sleep(random.randint(1, 2))
                        await message.channel.send(random.choice(responses), allowed_mentions=discord.AllowedMentions.none(), reference=message)
                        return

                    # Send request to ShuttleAI
                    chunks = []
                    sent_message = None
                    message_content = ""
                    build_messages = [{'role': 'system', 'content': instructions}] + conversation.get_messages()
                    try:
                        async with self.bot.session.post("https://api.shuttleai.app/v1/chat/completions", data=orjson.dumps({'model': model, 'messages': build_messages, 'stream': True, 'internet': False}).decode(), headers={'Authorization': f'Bearer {SHUTTLEAI_API_KEY}', 'Content-Type': 'application/json'}) as response:
                            async for line in response.content:
                                try:
                                    # Check if line is valid
                                    if line.startswith(b'data: '):
                                        jschunk = line[6:]
                                        try:
                                            jschunk = orjson.loads(jschunk)
                                            chunk = jschunk.get('choices', [{}])[0].get('delta', {}).get('content')
                                            # Append valid chunk
                                            if (chunk):
                                                chunks.append(chunk)
                                                message_content += chunk
                                        except:
                                            pass

                                        # Check for if the message is over discord's max char limit
                                        if len(message_content) > 2000:
                                            if not sent_message:
                                                sent_message = await message.channel.send(message_content[:2000], allowed_mentions=discord.AllowedMentions.none(), reference=message)
                                            else:
                                                await sent_message.edit(content=sent_message.content + message_content[:2000], allowed_mentions=discord.AllowedMentions.none())
                                                sent_message = await message.channel.fetch_message(sent_message.id)

                                            message_content = message_content[2000:]

                                        # Stream only if double line breaks found
                                        if "\n\n" in message_content or "\r" in message_content or "\r\n" in message_content:
                                            if not sent_message:
                                                sent_message = await message.channel.send(message_content, allowed_mentions=discord.AllowedMentions.none(), reference=message)
                                            else:
                                                await sent_message.edit(content=sent_message.content + '\n\n' + message_content, allowed_mentions=discord.AllowedMentions.none())
                                                sent_message = await message.channel.fetch_message(sent_message.id)
                                            message_content = ""
                                        else:
                                            pass
                                    else:
                                        pass
                                except Exception as e:
                                    log.error(f'ShuttleAI Request -> {e}')
                                    if "Must be" in str(e):
                                        sent_message = None
                                    if "rate limit" in str(e):
                                        await asyncio.sleep(1)
                                    pass

                            # Send the message chunk(s)
                            while len(message_content) > 0:
                                if not sent_message:
                                    sent_message = await message.channel.send(message_content[:2000], allowed_mentions=discord.AllowedMentions.none(), reference=message)
                                else:
                                    await sent_message.edit(content=sent_message.content + '\n\n' + message_content[:2000], allowed_mentions=discord.AllowedMentions.none())
                                message_content = message_content[2000:]

                    except Exception as e:
                        log.error(f'ShuttleAI Request -> {e}')
                        if "Must be" in str(e):
                            sent_message = None
                        if "rate limit" in str(e):
                            await asyncio.sleep(1)
                        pass

                    # Add assistant response to conversation
                    assistant_response = "".join(chunks)
                    conversation.add_message("assistant", assistant_response)

                    # Send DYK embed if able
                    if discord_id not in self.user_response_counter:
                        self.user_response_counter[discord_id] = 0
                    self.user_response_counter[discord_id] += 1   
                    if self.user_response_counter[discord_id] == 1:
                        if message.guild:
                            permissions = message.channel.permissions_for(message.guild.me)
                            can_send_embed = permissions.embed_links
                        else:
                            can_send_embed = True

                        if can_send_embed:
                            embed = discord.Embed(title=":poop: Imagine", description="Generate AI images using `/imagine` back up and working again! (fr this time). i used poop emoji to catch ur attention fr", color=discord.Color(0x2b2d31))
                            button = discord.ui.Button(label="Powered by ShuttleAI", url="https://shuttleai.app/?utm_source=discord&utm_medium=chat&utm_campaign=ShuttleAI+Discord+Bot", style=discord.ButtonStyle.url)
                            view = discord.ui.View()
                            view.add_item(button)
                            await message.channel.send(embed=embed, view=view)
                        else:
                            plain_message = "> **:poop: Imagine\n> Generate AI images using `/imagine` back up and working again!**"
                            await message.channel.send(plain_message)
                    if self.user_response_counter[discord_id] == 5:
                        self.user_response_counter[discord_id] = 0 
                    
                    # Handle TTS if enabled
                    if user_settings.get('tts', False) and assistant_response < 200:
                        pass # TODO: Send shuttleai tts request and send audio response

            except Exception as e:
                log.error(f"OnMessage Error -> {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(MessageCog(bot))