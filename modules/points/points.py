from discord.ext import commands
from discord import Member
from core.util import fileio
import pickle


class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = fileio.FileIO("points", "points")
        self.point_lists = self.load_data()

    @commands.group(name="points", aliases=["tcn"])
    @commands.guild_only()
    async def points_group(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @points_group.command(name="add")
    async def points_add(self, ctx, recipient: Member, points: int):
        # If no PointList exists for this user, make one
        if ctx.author.id not in self.point_lists:
            self.point_lists[ctx.author.id] = PointList(ctx.author.id)

        # Add points
        self.point_lists[ctx.author.id].add_points(recipient.id, abs(points))
        self.save_data()
        await ctx.send("Added points")

    @points_group.command(name="remove")
    async def points_remove(self, ctx, recipient: Member, points: int):
        # If no PointList exists for this user, make one
        if ctx.author.id not in self.point_lists:
            self.point_lists[ctx.author.id] = PointList(ctx.author.id)

        # Remove points
        self.point_lists[ctx.author.id].remove_points(recipient.id, abs(points))
        self.save_data()
        await ctx.send("Removed points")

    @points_group.command(name="redeem")
    async def points_redeem(self, ctx, target_economy: Member, points: int):
        # If no PointList exists for this user, make one
        if target_economy.id not in self.point_lists:
            self.point_lists[target_economy.id] = PointList(target_economy.id)

        # Redeem points
        status = self.point_lists[target_economy.id].redeem_points(ctx.author.id, abs(points))
        if status:
            self.save_data()
            await ctx.send("Redeemed points!")
        else:
            await ctx.send("Insufficient points!")

    def save_data(self):
        file = self.file.open("wb")
        pickle.dump(self.point_lists, file)
        file.close()

    def load_data(self):
        file = self.file.open("rb")
        try:
            return pickle.load(file)
        except EOFError:
            return {}
        finally:
            file.close()


class PointList:
    def __init__(self, owner_id: str):
        self.owner_id = owner_id  # ID of list owner
        self.points = {}  # Dict of (ID, Point) pairs

    def add_points(self, recipient_id: int, points: int):
        if recipient_id not in self.points:
            self.points[recipient_id] = Point(points)
        else:
            self.points[recipient_id].points = self.points[recipient_id].points + points

    def remove_points(self, recipient_id: int, points: int):
        if recipient_id in self.points:
            self.points[recipient_id].points = self.points[recipient_id].points - points
        else:
            self.points[recipient_id] = Point(0 - points)

    def redeem_points(self, recipient_id: int, points: int):
        if recipient_id in self.points:
            if self.points[recipient_id].points >= points:  # If points exist and have enough
                self.points[recipient_id].points = self.points[recipient_id].points - points
                self.points[recipient_id].redeemed_points += points
                return True
        else:
            # Has no points to redeem
            # Make point object for later reference
            self.points[recipient_id] = Point(0 - points)
            return False


class Point:
    def __init__(self, initial_points: int):
        self.points = initial_points
        self.redeemed_points = 0


def setup(bot):
    bot.add_cog(Points(bot))
