import aiohttp
import config
import discord
import traceback
from os import sep
from glob import iglob
from discord.ext import commands
from datetime import datetime


def _get_prefix(bot, message):
    prefixes = config.bot_prefixes

    # Allow only ! in PM
    if not message.guild:
        return '!'

    # Allow multiple prefixes while not in a PM
    return commands.when_mentioned_or(*prefixes)(bot, message)


class Cake(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=_get_prefix, description="A Modular Cakebot!",
                         fetch_offline_members=False)

        self.extensions_dir = "slices"
        self.start_time = None
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.approved_bots = config.approved_bots
        self.default_color = config.default_color

        # Load extensions from folders
        for extension in iglob(self.extensions_dir + "/**/*.py", recursive=True):
            extension = extension.replace(".py", '').replace(sep, '.')
            try:
                self.load_extension(extension)
                print(f'Loaded module {extension}')
            except (discord.ClientException, ModuleNotFoundError):
                print(f"Failed to load module {extension}.")
                traceback.print_exc()

    async def on_ready(self):
        # Set uptime
        if self.start_time is None:
            self.start_time = datetime.utcnow()

        # Set presence
        game = discord.Activity(name="!help", type=discord.ActivityType.listening)
        await self.change_presence(activity=game)

        print(f"Logged in as: {self.user.name} - {self.user.id}\nVersion: {discord.__version__}\n")
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
        await super().close()
        await self.session.close()

    def run(self):
        try:
            super().run(config.bot_token, bot=True, reconnect=True)
        except:
            print("Unable to start bot!")


if __name__ == '__main__':
    cake = Cake()
    cake.run()
