from discord import Embed
from discord.ext import commands
try:
    from bs4 import BeautifulSoup
    soup_available = True
except:
    soup_available = False


class Gruntle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_image(self):
        async with self.bot.session.get("https://www.gruntle.me") as r:
            if r.status == 200:
                text = await r.text()
                soup = BeautifulSoup(text, 'html.parser')
                image = soup.find("img", {"title": "un-disgruntle yourself with this!"})
                return "https://www.gruntle.me" + image['src'][1:]
            else:
                return None

    @commands.command(name='gruntle', alias=['cute'])
    @commands.guild_only()
    async def gruntle(self, ctx):
        image_url = await self.get_image()
        if image_url is None:
            embed = Embed(color=0xFDFBF7, description=":x: Error retrieving image!")
        else:
            embed = Embed(color=0xFDFBF7, title="Gruntle.me", url=image_url)
            embed.set_image(url=image_url)
        await ctx.send(embed=embed)


def setup(bot):
    if soup_available:
        bot.add_cog(Gruntle(bot))
    else:
        raise RuntimeError("Error: beautifulsoup4 not installed")
