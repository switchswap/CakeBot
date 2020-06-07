import aiohttp
import traceback
from os import sep
from glob import iglob
from discord.ext import commands
from datetime import datetime
from discord import __version__, Activity, ActivityType, ClientException
from core.util import config_manager
from typing import List
import asyncio


def _get_prefix(bot, message):
    prefixes = config_loader.load_key("bot_prefixes", "list of characters")

    # Allow only ! in PM
    if not message.guild:
        return '!'

    # Allow multiple prefixes while not in a PM
    return commands.when_mentioned_or(*prefixes)(bot, message)


class RoboSwap(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=_get_prefix, description="A Modular SwapBot!",
                         fetch_offline_members=False)

        self.prefixes = config_manager.load_key("bot_prefixes", List[str])
        self.extensions_dir = "modules"
        self.start_time = None
        self.approved_bots = config_manager.load_key("approved_bots", List[int])
        self.default_color = config_manager.load_key("default_color", List[int])
        self.bot_token = config_manager.load_key("bot_token", str)
        self.session = None

        # Load extensions from folders
        for module in iglob(self.extensions_dir + "/**/*.py", recursive=True):
            module = module.replace(".py", '').replace(sep, '.')
            try:
                self.load_extension(module)
                print(f'Loaded module {module}')
            except (ClientException, ModuleNotFoundError):
                print(f"Failed to load module {module}.")
                traceback.print_exc()

    async def loop_presence(self):
        """
        Reload presence every 45 minutes
        """
        await self.wait_until_ready()
        while not self.is_closed():
            # Set presence
            print("Setting activity...")
            # Todo: Remove hardcoded help command
            game = Activity(name="!help", type=ActivityType.listening)
            await self.change_presence(activity=game)
            print("Waiting 45 minutes...")
            await asyncio.sleep(2700)  # 45 minutes in seconds

    async def create_aiohttp_session(self):
        """
        Create aiohttp ClientSession
        """
        self.session = aiohttp.ClientSession(loop=self.loop)
        print("Created aiohttp ClientSession")

    async def on_ready(self):
        # Create task to create an aiohttp ClientSession
        self.loop.create_task(self.create_aiohttp_session())
        print("Create ClientSession task set")

        # Create task to reset the bot presence since it disappears occasionally
        self.loop.create_task(self.loop_presence())
        print("Presence task set")

        # Set uptime
        if self.start_time is None:
            self.start_time = datetime.utcnow()

        print(f"\nLogged in as: {self.user.name} - {self.user.id}\nVersion: {discord.__version__}\n")
        print("Successfully logged in!")
        print("-------------------")
        print("Servers connected to:")
        for guild in self.guilds:
            print(guild.name)
        print("-------------------")

    async def on_message(self, message):
        await self.process_commands(message)

    async def process_commands(self, message):
        if message.author.bot and message.author.id not in self.approved_bots:
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)

    async def on_resumed(self):
        print("Resuming...")

    async def close(self):
        await self.session.close()
        await super().close()

    def run(self):
        try:
            super().run(self.bot_token, bot=True, reconnect=True)
        except:
            print("Unable to start bot!")


if __name__ == '__main__':
    bot = RoboSwap()
    bot.run()
