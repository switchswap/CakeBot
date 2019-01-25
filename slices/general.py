from discord.ext import commands


class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add', aliases=['plus'])
    @commands.guild_only()
    async def do_addition(self, ctx, first: int, second: int):
        total = first + second
        await ctx.send(f'The sum of **{first}** and **{second}**  is  **{total}**')

    @commands.command(name='ping')
    async def only_me(self, ctx):
        await ctx.send("pong!")

    @commands.command(name='me')
    @commands.is_owner()
    async def only_me(self, ctx):
        await ctx.send(f'Hello {ctx.author.mention}. This command can only be used by you!!')



# Important!
def setup(bot):
    bot.add_cog(General(bot))
