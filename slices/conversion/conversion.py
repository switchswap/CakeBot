from discord import Embed
from discord.ext import commands


class Conversion(commands.Cog):
    """
    Conversion class containing a few unit conversion functions
    Can be used in DM's as well as in Guild
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='c2f')
    async def celsius_to_fahrenheit(self, ctx, num: float):
        """
        Convert celsius to fahrenheit
        """
        value = round((num * 1.8) + 32, 2)
        embed = Embed(color=self.bot.default_color)
        embed.add_field(name="Fahrenheit", value=f"{value} °F")
        await ctx.send(embed=embed)

    @commands.command(name='f2c')
    async def fahrenheit_to_celsius(self, ctx, num: float):
        """
        Convert fahrenheit to celsius
        """
        value = round((num - 32) / 1.8, 2)
        embed = Embed(color=self.bot.default_color)
        embed.add_field(name="Celsius", value=f"{value} °C")
        await ctx.send(embed=embed)

    @commands.command(name='cm2ft')
    async def cm_to_feet(self, ctx, num: float):
        """
        Convert cm to feet
        """
        value = round(num / 30.48, 3)
        embed = Embed(color=self.bot.default_color)
        embed.add_field(name="Feet", value=f"{value} ft")
        await ctx.send(embed=embed)

    @commands.command(name='ft2cm')
    async def feet_to_cm(self, ctx, num: float):
        """
        Convert feet to cm
        """
        value = round(num * 30.48, 3)
        embed = Embed(color=self.bot.default_color)
        embed.add_field(name="Centimeters", value=f"{value} cm")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Conversion(bot))
