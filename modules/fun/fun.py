from discord import Embed, Member
from discord.ext import commands


class Fun(commands.Cog):
    """
    Fun functions!
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fact")
    @commands.guild_only()
    async def fun_fact(self, ctx):
        async with ctx.typing():
            data = await self._get_data("https://useless-facts.sameerkumar.website/api")
        if data is not None:
            embed = Embed(color=self.bot.default_color, title="Fun fact!", description=data["data"])
        else:
            embed = Embed(color=self.bot.default_color, description=":x: Error talking to api!")
        await ctx.send(embed=embed)

    @commands.command(name="joke", aliases=["dadjoke"])
    @commands.guild_only()
    async def dad_joke(self, ctx):
        async with ctx.typing():
            data = await self._get_data("https://dadjoke-api.herokuapp.com/api/v1/dadjoke")
        if data is not None:
            embed = Embed(color=self.bot.default_color, title="Dad joke", description=data["joke"])
        else:
            embed = Embed(color=self.bot.default_color, description=":x: Error talking to api!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def corona(self, ctx, country_code=None):
        if country_code is not None:
            url = f"https://api.thevirustracker.com/free-api?countryTotal={country_code}"
        else:
            url = "https://api.thevirustracker.com/free-api?global=stats"

        async with ctx.typing():
            data = await self._get_data(url)
        if data is not None and "data" not in data["results"][0]:
            embed = Embed(color=self.bot.default_color)
            embed.add_field(name="Total Cases", value=data["results"][0]["total_cases"], inline=False)
            embed.add_field(name="Recovered", value=data["results"][0]["total_recovered"], inline=False)
            embed.add_field(name="Unresolved", value=data["results"][0]["total_unresolved"], inline=False)
            embed.add_field(name="Deaths", value=data["results"][0]["total_deaths"], inline=False)
            embed.add_field(name="Active Cases", value=data["results"][0]["total_active_cases"], inline=False)
            embed.add_field(name="New Cases Today", value=data["results"][0]["total_new_cases_today"], inline=False)
            if country_code is None:
                embed.add_field(name="Affected Countries", value=data["results"][0]["total_affected_countries"],
                                inline=False)
            else:
                embed.add_field(name="Danger Rank", value=data["results"][0]["total_danger_rank"], inline=False)
        elif data is not None and "data" in data["results"][0]:
            embed = Embed(color=self.bot.default_color, description=":x: Invalid country code!")
        else:
            embed = Embed(color=self.bot.default_color, description=":x: Error talking to api!")
        await ctx.send(embed=embed)

    @commands.command(aliases=['discrim'])
    @commands.guild_only()
    async def discriminators(self, ctx):
        discriminator = ctx.author.discriminator
        count = 0
        for member in ctx.guild.members:
            if member.discriminator == discriminator and member != ctx.author:
                count += 1
        embed = Embed(color=self.bot.default_color,
                      description=f"You share the discriminator {ctx.author.discriminator} with {count} other(s)!")
        await ctx.send(embed=embed)
        # Todo: Pagination to list the users

    @commands.command(hidden=True)
    @commands.guild_only()
    async def say(self, ctx, *, message):
        if await self.bot.is_owner(ctx.author) or ctx.author.guild_permissions.administrator:
            if ctx.guild.me.guild_permissions.manage_messages:
                await ctx.message.delete()
            await ctx.send(message)
        else:
            await ctx.send(f"Don't tell me what to say {ctx.author.mention}!")

    @commands.command(name="didyoumean", aliases=["dym"])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def did_you_mean(self, ctx, *, message):
        embed = Embed(color=self.bot.default_color)
        message = message.replace(' ', '%20')
        message_array = message.split("\\\\")
        if len(message_array) != 2:
            embed.description = ":x: Invalid arguments!"
        else:
            embed.set_image(url=f"https://api.alexflipnote.dev/didyoumean?top={message_array[0]}"
                                f"&bottom={message_array[1]}")
        await ctx.send(embed=embed)

    @commands.command(name="changemymind", aliases=["cmm"])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def change_my_mind(self, ctx, *, message):
        message = message.replace(' ', "%20")
        async with ctx.typing():
            data = await self._get_data(f"https://nekobot.xyz/api/imagegen?type=changemymind&text={message}")
        embed = Embed(color=self.bot.default_color)
        if data is not None:
            embed.set_image(url=data["message"])
        else:
            embed.description = ":x: Error talking to api!"
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def bored(self, ctx):
        async with ctx.typing():
            data = await self._get_data("http://www.boredapi.com/api/activity/")
        embed = Embed(color=self.bot.default_color)
        if data is not None:
            embed.title = "Bored? Try this!"
            embed.description = f'{data["activity"]}!'
        else:
            embed.description = ":x: Error talking to api!"
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def clap(self, ctx, *, message: str):
        await ctx.send(message.replace(' ', " 👏 "))

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def bedtime(self, ctx, member: Member):
        try:
            await member.send("Someone who cares about you says it's time to go to sleep now! Goodnight!")
            if ctx.guild.me.guild_permissions.manage_messages:
                await ctx.message.delete()
        except:
            await member.send("I couldn't message them! They probably have me blocked...s :sob:")

    async def _get_data(self, url):
        async with self.bot.session.get(url) as r:
            if r.status == 200:
                return await r.json()
            else:
                return None


def setup(bot):
    bot.add_cog(Fun(bot))
