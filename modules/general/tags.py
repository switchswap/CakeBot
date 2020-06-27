import pickle
from core.util import fileio
from discord import Embed
from discord.ext import commands


class Tags(commands.Cog):
    """
    Tag storing functions
    """
    def __init__(self, bot):
        self.bot = bot
        self.file = fileio.FileIO("tags", "tags")
        self.tags = self._load_data()
        self.partial_tags = {}

    @commands.group()
    @commands.guild_only()
    async def tag(self, ctx):
        if ctx.invoked_subcommand is None:
            tag = self._find_tag(ctx.message.content[len(ctx.prefix + ctx.invoked_with) + 1:], ctx.guild.id)
            if tag is not None:
                await ctx.send(tag["content"])
            else:
                await ctx.send("Tag not found!")

    @tag.command()
    async def make(self, ctx, *, tag_name: str):
        if self._tag_in_use(tag_name, ctx.guild.id):
            await ctx.send("That tag currently being modified!")
        elif not self._tag_exists(tag_name, ctx.guild.id) and self._check_valid_name(tag_name):
            self._mark_tag_in_use(tag_name, ctx.guild.id)
            await ctx.send(f"What are the contents of {tag_name}? **Type `abort` to cancel.**")

            def check(m):
                return m.channel.id == ctx.channel.id and m.author == ctx.author

            response = await self.bot.wait_for('message', check=check)
            if response.content.lower() == "abort":
                self._unmark_tag_in_use(tag_name, ctx.guild.id)
                await ctx.send("Canceled.")
                return

            self._save_tag(tag_name, response)
            self._unmark_tag_in_use(tag_name, ctx.guild.id)
            await ctx.send("Tag set!")
        else:
            await ctx.send("That tag already exists!")

    @tag.command()
    async def edit(self, ctx, *, tag_name: str):
        tag = self._find_tag(tag_name, ctx.guild.id)
        if tag is not None and \
                not await self.has_perms(tag["owner"], ctx.author):
            await ctx.send("That tag doesn't belong to you!")
        elif not self._tag_in_use(tag_name, ctx.guild.id):
            self._mark_tag_in_use(tag_name, ctx.guild.id)
            await ctx.send("What would you like to replace the contents of this tag with? **Type `abort` to cancel.**")
        else:
            await ctx.send("That tag currently being modified!")
            return

        def check(m):
            return m.channel.id == ctx.channel.id and m.author == ctx.author

        response = await self.bot.wait_for('message', check=check)
        if response.content.lower() == "abort":
            self._unmark_tag_in_use(tag_name, ctx.guild.id)
            await ctx.send("Canceled.")
            return

        self._unmark_tag_in_use(tag_name, ctx.guild.id)
        self._save_tag(tag_name, response)
        await ctx.send("Tag set!")

    @tag.command()
    async def claim(self, ctx, *, tag_name: str):
        tag = self._find_tag(tag_name, ctx.guild.id)
        if tag is not None:
            if ctx.guild.get_member(tag["owner"]) is None or self.has_perms(tag["owner"], ctx.author):
                self.tags[ctx.guild.id][tag_name]["owner"] = ctx.author.id
                self._save_data()
                await ctx.send("You are now the owner of this tag!")
            else:
                await ctx.send("Tag owner is still in guild!")
        else:
            await ctx.send("That tag doesn't exist!")
        pass

    @tag.command()
    async def info(self, ctx, *, tag_name):
        tag = self._find_tag(tag_name, ctx.guild.id)
        if tag is not None:
            owner = ctx.guild.get_member(tag["owner"])
            creation_date = tag["creation_date"].strftime('%m-%d-%Y %H:%M:%S UTC')
            embed = Embed(color=self.bot.default_color)
            embed.set_author(name=f"{owner}", icon_url=owner.avatar_url)
            embed.title = tag["name"]
            embed.add_field(name="Owner", value=owner.mention)
            embed.set_footer(text=f"Created at {creation_date}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("That tag doesn't exist!")

    @commands.command()
    @commands.guild_only()
    async def tags(self, ctx):
        # Get all the user tags
        tags = []

        tags_string = ""
        if ctx.guild.id in self.tags:
            for key in self.tags[ctx.guild.id]:
                if self.tags[ctx.guild.id][key]["owner"] == ctx.author.id:
                    tags.append(self.tags[ctx.guild.id][key]["name"])

            for tag in tags:
                tags_string += tag + "\n"

        embed = Embed(color=self.bot.default_color)
        embed.set_author(name=f"{ctx.author}'s Tags", icon_url=ctx.author.avatar_url)
        embed.description = tags_string
        await ctx.send(embed=embed)

    def _save_tag(self, tag_name, response):
        response_text = response.clean_content
        if len(response.attachments) > 0:
            for attachment in response.attachments:
                response_text += "\n" + attachment.url
        if response.guild.id not in self.tags:
            self.tags[response.guild.id] = {}
        self.tags[response.guild.id][tag_name.lower()] = {
            "name": tag_name,
            "content": response_text,
            "owner": response.author.id,
            "creation_date": response.created_at
        }
        self._save_data()

    def _mark_tag_in_use(self, tag_name, guild_id):
        if guild_id not in self.partial_tags:
            self.partial_tags[guild_id] = {}
        self.partial_tags[guild_id][tag_name.lower()] = {}
        return

    def _unmark_tag_in_use(self, tag_name, guild_id):
        del self.partial_tags[guild_id][tag_name.lower()]

    def _save_data(self):
        file = self.file.open("wb")
        pickle.dump(self.tags, file)
        file.close()

    def _load_data(self):
        file = self.file.open("rb")
        try:
            return pickle.load(file)
        except EOFError:
            return {}
        finally:
            file.close()

    async def has_perms(self, tag_owner, author):
        if author.guild_permissions.administrator:
            return True
        if author.id == tag_owner:
            return True
        if await self.bot.is_owner(author):
            return True
        return False

    def _tag_exists(self, tag_name, guild_id):
        tag_name = tag_name.lower()
        if guild_id in self.tags and tag_name in self.tags[guild_id]:
            return True
        return False

    def _tag_in_use(self, tag_name, guild_id):
        tag_name = tag_name.lower()
        if guild_id in self.partial_tags and tag_name in self.partial_tags[guild_id]:
            return True
        return False

    def _find_tag(self, tag_name, guild_id):
        tag_name = tag_name.lower()
        if guild_id in self.tags and tag_name in self.tags[guild_id]:
            return self.tags[guild_id][tag_name]
        return None

    @staticmethod
    def _check_valid_name(tag_name):
        invalid_tags = {"make", "info", "claim", "edit"}
        return tag_name not in invalid_tags


def setup(bot):
    bot.add_cog(Tags(bot))
