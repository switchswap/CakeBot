from discord import Embed, Emoji
from discord.ext import commands


class Stats(commands.Cog):
    """
    Functions that relate to stats
    """

    def __init__(self, bot):
        self.bot = bot

    async def chat_counts(self, ctx):
        pass

    async def channel_stats(self, ctx):
        # channel stats like when created
        pass

    async def guild_stats(self, ctx):
        pass

    @commands.command(name="emoji")
    @commands.guild_only()
    async def emoji_info(self, ctx, emoji: Emoji):
        embed = Embed(title='Emoji Information', color=self.bot.default_color)
        embed.add_field(name='Name', value=f':{emoji.name}:', inline=False)
        embed.add_field(name='ID', value=f'{str(emoji.id)}', inline=False)
        emoji_guild = self.bot.get_guild(emoji.guild_id)
        embed.add_field(name='Origin Server', value=emoji_guild.name, inline=False)
        if emoji.guild_id == ctx.guild.id and ctx.guild.me.guild_permissions.manage_emojis:
            emoji_data = await ctx.guild.fetch_emoji(emoji.id)
            embed.add_field(name="Emoji created by", value=emoji_data.user, inline=False)
        embed.set_thumbnail(url=str(emoji.url))
        embed.set_footer(text="Emoji created at " + emoji.created_at.strftime("%m-%d-%Y %H:%M:%S UTC"))
        await ctx.send(embed=embed)

    @emoji_info.error
    async def run_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = Embed(color=self.bot.default_color, description=":x: Must be a custom emote!")
            await ctx.send(embed=embed)
        else:
            raise error


def setup(bot):
    bot.add_cog(Stats(bot))
