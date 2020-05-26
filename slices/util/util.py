import os
import asyncio
from datetime import datetime
from discord import Embed, __version__, Activity, ActivityType
from discord.ext import commands
from platform import python_version
try:
    import psutil
    psutil_available = True
except:
    psutil_available = False


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.presence_task = self.bot.loop.create_task(self.loop_presence())

    # Return uptime of bot
    def _get_uptime(self):
        time_diff = datetime.utcnow() - self.bot.start_time
        uptime = f'{time_diff.days}d {time_diff.seconds//3600}h {(time_diff.seconds//60)%60}m'
        return uptime

    # Return memory usage of bot
    def _get_mem_usage(self):
        mem_usage = float(psutil.Process(os.getpid()).memory_info().rss)/1000000
        return str(round(mem_usage, 2)) + " MB"

    @commands.command(name='leave_guild', aliases=['leave'], hidden=True)
    @commands.is_owner()
    async def leave_guild(self, name: str):
        for guild in self.bot.guilds:
            if guild.name == name:
                await guild.leave()

    # Return all guilds the bot is in
    @commands.command(name='list_guilds', aliases=['list'], hidden=True)
    @commands.is_owner()
    async def list_guilds(self, ctx):
        guilds = ""
        for guild in self.bot.guilds:
            guilds += guild.name + "\n"

        embed = Embed(color=self.bot.default_color)
        embed.add_field(name="Guilds", value=guilds)
        await ctx.send(embed=embed)

    # Display bot info
    @commands.command(name="info")
    async def info(self, ctx):
        embed = Embed(color=self.bot.default_color)
        embed.add_field(name="Memory", value=self._get_mem_usage(), inline=True)
        embed.add_field(name="Python", value=python_version(), inline=True)
        embed.add_field(name="discord.py", value=__version__, inline=True)
        embed.add_field(name="Slices", value=str(len(self.bot.cogs.keys())), inline=True)
        embed.add_field(name="Guilds", value=str(len(self.bot.guilds)), inline=True)
        embed.add_field(name="Uptime", value=self._get_uptime(), inline=True)
        embed.set_footer(text="This is an instance of Cakebot created by `Switch#8155`!")
        await ctx.send(embed=embed)

    # Unload slice
    @commands.command(name="unload", hidden=True)
    @commands.is_owner()
    async def unload_slice(self, ctx, *, name):
        description = ":white_check_mark: Successfully unloaded slice!"
        try:
            self.bot.unload_extension(name)
        except commands.ExtensionNotLoaded:
            description = ":x: Slice not loaded!"

        embed = Embed(color=self.bot.default_color)
        embed.description = description
        print(f'Unloaded module {name}')
        await ctx.send(embed=embed)

    # Load slice
    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def load_slice(self, ctx, *, name):
        description = ":white_check_mark: Successfully loaded slice!"
        try:
            self.bot.load_extension(name)
        except commands.ExtensionNotFound:
            description = ":x: Slice could not be found!"
        except commands.ExtensionAlreadyLoaded:
            description = ":x: Slice already loaded!"
        except commands.NoEntryPointError:
            description = ":x: The slice does not have a setup function!"
        except commands.ExtensionFailed:
            description = ":x: Error in the slice setup function!"

        embed = Embed(color=self.bot.default_color)
        embed.description = description
        print(f'Loaded module {name}')
        await ctx.send(embed=embed)

    # Reload slice
    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload_slice(self, ctx, *, name):
        description = ":white_check_mark: Successfully reloaded slice!"
        try:
            self.bot.reload_extension(name)
        except commands.ExtensionNotLoaded:
            description = ":x: Could not reload slice!"
        except commands.ExtensionNotFound:
            description = ":x: Slice could not be found!"
        except commands.NoEntryPointError:
            description = ":x: The slice does not have a setup function!"
        except commands.ExtensionFailed:
            description = ":x: Error in the slice setup function!"

        embed = Embed(color=self.bot.default_color)
        embed.description = description
        print(f'Reloaded module {name}')
        await ctx.send(embed=embed)

    # Reload presence every 45 minutes
    async def loop_presence(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            # Set presence
            print("Setting activity...")
            game = Activity(name="!help", type=ActivityType.listening)
            await self.bot.change_presence(activity=game)
            print("Waiting 45 minutes...")
            await asyncio.sleep(2700)  # 45 minutes in seconds


def setup(bot):
    if psutil_available:
        bot.add_cog(Util(bot))
    else:
        raise RuntimeError("Error: psutil not installed")
