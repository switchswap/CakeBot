import os
import traceback
from datetime import datetime
from discord import Embed, __version__
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
        embed.set_footer(text="This is an instance of Cakebot created by Switch!")
        await ctx.send(embed=embed)

    # Unload slice
    @commands.command(name="unload", hidden=True)
    @commands.is_owner()
    async def unload_slice(self, ctx, *, name):
        try:
            self.bot.unload_extension(name)
        except Exception:
            embed = Embed(color=self.bot.default_color)
            embed.description = ":x: Could not unload slice!"
            print(traceback.format_exc())
        else:
            embed = Embed(color=self.bot.default_color)
            embed.description = ":white_check_mark: Successfully unloaded slice!"
        await ctx.send(embed=embed)

    # Load slice
    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def load_slice(self, ctx, *, name):
        try:
            self.bot.load_extension(name)
        except Exception:
            embed = Embed(color=self.bot.default_color)
            embed.description = ":x: Could not load slice!"
            print(traceback.format_exc())
        else:
            embed = Embed(color=self.bot.default_color)
            embed.description = ":white_check_mark: Successfully loaded slice!"
        await ctx.send(embed=embed)

    # Reload slice
    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload_slice(self, ctx, *, name):
        try:
            self.bot.unload_extension(name)
            self.bot.load_extension(name)
        except Exception:
            embed = Embed(color=self.bot.default_color)
            embed.description = ":x: Could not reload slice!"
            print(traceback.format_exc())
        else:
            embed = Embed(color=self.bot.default_color)
            embed.description = ":white_check_mark: Successfully reloaded slice!"
        await ctx.send(embed=embed)


def setup(bot):
    if psutil_available:
        bot.add_cog(Util(bot))
    else:
        raise RuntimeError("Error: psutil not installed")
