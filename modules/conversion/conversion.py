from discord import Embed
from discord.ext import commands
from dataclasses import dataclass
import re


class Conversion(commands.Cog):
    """
    Conversion class containing a few unit conversion functions
    Can be used in DM's as well as in Guild
    """

    def __init__(self, bot):
        self.bot = bot
        self.valid_conversions = {
            "f": {"c": self.feet_to_centimeters},
            "c": {"f": self.centimeters_to_feet},
            "mph": {"kph": self.mph_to_kph},
            "kph": {"mph": self.kph_to_mph},
            "ft": {"cm": self.feet_to_centimeters, "m": self.feet_to_meters, "in": self.feet_to_inches},
            "in": {"ft": self.inches_to_feet},
            "cm": {"ft": self.centimeters_to_feet, "m": self.centimeters_to_meters},
            "m": {"cm": self.meters_to_centimeters, "ft": self.meters_to_feet}
        }
        self.valid_units = "|".join(list(self.valid_conversions.keys()))

    @commands.command(name="convert")
    @commands.guild_only()
    async def convert(self, ctx, *, message: str):
        """
        Convert something to given unit

        Will parse text and pick the right command to execute
        """
        matches = re.match(
            "^([+-]?\d+(\.\d{1,10})?)" + f"({self.valid_units}) +({self.valid_units})$", message)
        if matches is None:
            embed = Embed(color=self.bot.default_color,
                          description=":x: I don't understand that!")
            await ctx.send(embed=embed)
            return

        groups = matches.groups()
        value = float(groups[0])
        initial_unit = groups[2]
        target_unit = groups[3]
        conversion_path = self.calculate_conversion_path(
            initial_unit, target_unit)

        if initial_unit == target_unit:
            description = ":o: Units are the same. No need for conversion!"
            embed = Embed(color=self.bot.default_color)
            embed.description = description
        elif conversion_path != "":
            await self.execute_conversion(ctx, value, conversion_path)
        else:
            embed = Embed(color=self.bot.default_color,
                          description=":x: I can't convert those units!")
            await ctx.send(embed=embed)

    async def execute_conversion(self, ctx, value: float, conversion_path: str):
        path = conversion_path.split(' ')

        temp = value
        while len(path) != 1:
            # Convert from first to second type
            temp = self.valid_conversions[path[0]][path[1]](value)

            # Remove first element in path since we've just converted from that
            path.pop(0)

        embed = Embed(color=self.bot.default_color)
        # At this point, path has been shrunk to length 1 so the first element is our target unit
        embed.add_field(name="Converted", value=f"{round(temp,3)}{path[0]}")
        await ctx.send(embed=embed)

    @staticmethod
    def celsius_to_fahrenheit(num: float):
        """
        Convert celsius to fahrenheit
        """
        return (num * 1.8) + 32

    @staticmethod
    def fahrenheit_to_celsius(num: float):
        """
        Convert fahrenheit to celsius
        """
        return (num - 32) / 1.8

    @staticmethod
    def meters_to_feet(num: float):
        """
        Convert m to feet
        """
        return num / 0.3048

    @staticmethod
    def centimeters_to_feet(num: float):
        """
        Convert cm to feet
        """
        return num / 30.48

    @staticmethod
    def feet_to_centimeters(num: float):
        """
        Convert feet to cm
        """
        return num * 30.48

    @staticmethod
    def feet_to_meters(num: float):
        """
        Convert feet to m
        """
        return num * 0.3048

    @staticmethod
    def inches_to_feet(num: float):
        """
        Convert inches to feet
        """
        return num / 12

    @staticmethod
    def feet_to_inches(num: float):
        """
        Convert feet to inches
        """
        return num * 12

    @staticmethod
    def mph_to_kph(num: float):
        """
        Convert MPH tp KPH
        """
        return num * 1.609344

    @staticmethod
    def kph_to_mph(num: float):
        """
        Convert KPH to MPH
        """
        return num * 0.6213712

    @staticmethod
    def centimeters_to_meters(num: float):
        """
        Convert cm to m
        """
        return num / 100

    @staticmethod
    def meters_to_centimeters(num: float):
        """
        Convert m to cm
        """
        return num * 100

    def calculate_conversion_path(self, initial_unit, target_unit):
        """
        Calculate path of conversion
        """
        visited_nodes = {initial_unit: 0}
        neighbors = []
        for new_neighbor in self.valid_conversions[initial_unit].keys():
            neighbors.append(
                UnitNode(new_neighbor, 1, f"{initial_unit} {new_neighbor}"))

        while len(neighbors) > 0:
            curr_node: UnitNode = neighbors.pop(0)

            # If curr node has not yet been visited
            if curr_node.unit not in visited_nodes:
                # Add to visited
                visited_nodes[curr_node.unit] = curr_node.distance

                if curr_node.unit == target_unit:
                    # This node completes the path
                    return curr_node.path

                # Get curr node neighbors
                new_neighbors = self.valid_conversions[curr_node.unit].keys()
                for new_neighbor in new_neighbors:
                    neighbors.append(UnitNode(
                        new_neighbor, curr_node.distance + 1, f"{curr_node.path} {new_neighbor}"))
        return ""


@dataclass
class UnitNode:
    unit: str
    distance: int
    path: str


def setup(bot):
    bot.add_cog(Conversion(bot))
