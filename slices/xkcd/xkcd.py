from discord.ext import commands
from random import randint
from discord import Embed
from time import time
import requests


class XKCD:
    def __init__(self, bot):
        self.bot = bot
        self.latest_comic = 1
        self.latest_update_time = 0

    async def update_latest(self):
        latest_xkcd = await self.get_xkcd()
        if latest_xkcd:
            self.latest_comic = latest_xkcd['num']
            self.latest_update_time = time()
        else:
            print("Could not update latest!")

    # Returns XKCD comic json given a number else returns the latest
    # Assumes given number is correct
    async def get_xkcd(self, number: int = None):
        url = "http://xkcd.com/info.0.json" if number is None else f'http://xkcd.com/{number}/info.0.json'
        async with self.bot.session.get(url) as r:
            if r.status == 200:
                data = await r.json()
                return data
            else:
                return None

    @commands.command(name="xkcd")
    @commands.guild_only()
    async def xkcd(self, ctx, number: str = None):
        # Check if latest is up to date
        if time() - self.latest_update_time > 86400:  # If over 24 hours in difference
            await self.update_latest()

        is_valid_number = True if number and number.isdigit() and int(number) <= self.latest_comic else False
        if is_valid_number:  # Find that specific XKCD
            xkcd_json = await self.get_xkcd(number)
        else:  # Find random XKCD
            xkcd_json = await self.get_xkcd(randint(1, self.latest_comic))

        if xkcd_json is None:
            embed = Embed(color=0xFFFFFF, description=":x: Problem retrieving XKCD!")
        else:
            embed = Embed(color=0xFFFFFF)
            embed.url = 'https://xkcd.com/{}/'.format(xkcd_json['num'])
            embed.title = '[XKCD #{}] {}'.format(xkcd_json['num'], xkcd_json['safe_title'])
            embed.set_image(url=xkcd_json['img'])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(XKCD(bot))
