from discord.ext import commands
from random import randint


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add', aliases=['plus'])
    @commands.guild_only()
    async def do_addition(self, ctx, first: int, second: int):
        total = first + second
        await ctx.send(f'The sum of **{first}** and **{second}**  is  **{total}**')

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send("pong!")

    @commands.command(name='owner')
    @commands.is_owner()
    async def owner_test(self, ctx):
        await ctx.send(f'Hello {ctx.author.mention}. This command can only be used by you!!')

    @commands.command(name="roll")
    @commands.guild_only()
    async def roll(self, ctx, boundary: str = None):
        valid_boundary = self._valid_boundary(boundary)
        if valid_boundary:
            await ctx.send(f"{ctx.author.mention} rolled {randint(1, int(boundary))}!")
        else:
            await ctx.send(f"{ctx.author.mention} rolled {randint(1, 100)}!")

    @staticmethod
    def _valid_boundary(number):
        # Number must exist
        if number is None:
            return False

        # Number must be a digit
        if not number.isdigit():
            return False

        # Number must be greater than 1
        if int(number) < 1:
            return False

        return True


def setup(bot):
    bot.add_cog(General(bot))
