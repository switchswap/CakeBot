from discord import Embed, Member
from discord.ext import commands
from random import randint
from datetime import datetime


class General(commands.Cog):
    """
    Basic functions for any bot
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """
        Hello world for bots
        """
        embed = Embed(color=self.bot.default_color)
        embed.title = "Pong!"
        embed.description = f"Latency: **{round(self.bot.latency * 1000, 2)}** ms"
        await ctx.send(embed=embed)

    @commands.command(name='owner')
    @commands.is_owner()
    async def owner_test(self, ctx):
        """
        Owner-only test command
        """
        await ctx.send(f'Hello {ctx.author.mention}. This command can only be used by you!')

    @commands.command(name='add', aliases=['plus'])
    @commands.guild_only()
    async def do_addition(self, ctx, first: int, second: int):
        """
        Add two numbers
        """
        total = first + second
        await ctx.send(f'The sum of **{first}** and **{second}**  is  **{total}**')

    @commands.command(name="roll")
    @commands.guild_only()
    async def roll(self, ctx, boundary: str = None):
        """
        Get a random number within a given boundary
        Default: 1-100
        """
        valid_boundary = self._valid_boundary(boundary)
        if valid_boundary:
            await ctx.send(f"{ctx.author.mention} rolled {randint(1, int(boundary))}!")
        else:
            await ctx.send(f"{ctx.author.mention} rolled {randint(1, 100)}!")

    @commands.command(name="snowflake")
    async def snowflake(self, ctx, snowflake: int):
        """
        Returns timestamp from discord id
        """
        unix = ((snowflake >> 22) + 1420070400000) / 1000
        readable_date = datetime.utcfromtimestamp(unix).strftime('%m-%d-%Y %H:%M:%S UTC')
        embed = Embed(color=self.bot.default_color)
        embed.add_field(name="Date", value=readable_date)
        await ctx.send(embed=embed)

    @commands.command(name="whois")
    @commands.guild_only()
    async def whois(self, ctx, member: Member):
        """
        Show user information
        """
        # Get user roles
        roles = "\n".join(role.name for role in member.roles)
        guild_join_date = member.joined_at.strftime('%m-%d-%Y %H:%M:%S UTC')
        discord_join_date = member.created_at.strftime('%m-%d-%Y %H:%M:%S UTC')
        nick = member.nick if member.nick is not None else "N/A"
        # Create response
        embed = Embed(color=self.bot.default_color)
        embed.set_author(name=f"{member}'s info")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.add_field(name="Name", value=f"{member.name}", inline=True)
        embed.add_field(name="Nick", value=f"{nick}", inline=True)
        embed.add_field(name="Roles", value=roles)
        # Guild join date can be None so default value is needed
        embed.add_field(name="Guild Join Date", value=guild_join_date if guild_join_date is not None else "N/A")
        embed.add_field(name="Discord Join Date", value=discord_join_date)
        await ctx.send(embed=embed)

    @commands.command(name="avatar")
    @commands.guild_only()
    async def avatar(self, ctx, member: Member = None):
        """
        Show user avatar
        """
        # Default to message author
        if member is None:
            member = ctx.author
        embed = Embed(color=self.bot.default_color)
        embed.title = f"{member.display_name}'s avatar"
        embed.url = str(member.avatar_url)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

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

    @staticmethod
    def _datetime_to_string(time: datetime) -> str:
        return time.strftime("%m/%d/%Y")


def setup(bot):
    bot.add_cog(General(bot))
