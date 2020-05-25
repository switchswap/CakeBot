from core.util import config_loader
from discord.ext import commands
from discord import Embed


class Osu(commands.Cog):
    API_KEY = config_loader.load_key("osu_api_key", "string")

    def __init__(self, bot):
        self.bot = bot

    async def get_user_stats(self, username: str, game_mode: int):
        api_endpoint = "https://osu.ppy.sh"
        params = {'k': self.API_KEY, 'u': username, 'm': game_mode}
        async with self.bot.session.get(api_endpoint + "/api/get_user", params=params) as r:
            if r.status == 200:
                return await r.json()
            else:
                return None

    def parse_stats(self, stats_json_array):
        if stats_json_array is None or len(stats_json_array) == 0:
            embed = Embed(color=0xFF66AA)
            embed.description = ":x: Could not find user!"
            return embed

        stats_json = stats_json_array[0]
        embed = Embed(title=f"Stats for {stats_json['username']}", url=f"https://osu.ppy.sh/u/{stats_json['user_id']}",
                      color=0xFF66AA)
        embed.set_thumbnail(url=f"https://a.ppy.sh/{stats_json['user_id']}")
        embed.add_field(name="Username", value=stats_json['username'], inline=True)
        embed.add_field(name="Country", value=stats_json['country'], inline=True)
        embed.add_field(name="Rank", value=stats_json['pp_rank'], inline=True)
        embed.add_field(name="Country Rank", value=stats_json['pp_country_rank'], inline=True)
        embed.add_field(name="PP", value=stats_json['pp_raw'], inline=True)
        embed.add_field(name="Accuracy", value=stats_json['accuracy'], inline=True)
        embed.add_field(name="Level", value=stats_json['level'], inline=True)
        embed.add_field(name="Play Count", value=stats_json['playcount'], inline=True)
        embed.set_footer(text="Powered by https://osu.ppy.sh")
        return embed

    @commands.command(name="osu")
    @commands.guild_only()
    async def osu_stats(self, ctx, username: str):
        stats_json_array = await self.get_user_stats(username, 0)
        embed = self.parse_stats(stats_json_array)
        await ctx.send(embed=embed)

    @commands.command(name="taiko")
    @commands.guild_only()
    async def taiko_stats(self, ctx, username: str):
        stats_json_array = await self.get_user_stats(username, 1)
        embed = self.parse_stats(stats_json_array)
        await ctx.send(embed=embed)

    @commands.command(name="ctb")
    @commands.guild_only()
    async def ctb_stats(self, ctx, username: str):
        stats_json_array = await self.get_user_stats(username, 2)
        embed = self.parse_stats(stats_json_array)
        await ctx.send(embed=embed)

    @commands.command(name="mania")
    @commands.guild_only()
    async def mania_stats(self, ctx, username: str):
        stats_json_array = await self.get_user_stats(username, 3)
        embed = self.parse_stats(stats_json_array)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Osu(bot))
