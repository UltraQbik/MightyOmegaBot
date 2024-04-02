"""
This is an example extension cog for MightyOmegaBot.
It shows you how to add your own cogs for the bot if you want to contribute.
"""


import discord
from discord import app_commands
from discord.ext import commands


class EXTExample(commands.Cog):
    """
    This is an example cog which adds example commands
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

        # here's an example variable
        self.example = "example"

        # here's an example path to the database
        self.db_path = "var/example_db.json"
        # it is much preferred if you store databases
        # in json format, and they must be stored in
        # 'var' folder, that will be created by the bot

    @app_commands.command(name="example", description="does some things")
    @app_commands.describe(
        message="Some kind of message")
    async def example(
        self,
        interaction: discord.Interaction,
        message: str
    ) -> None:
        """
        This is an example slash command
        """

        pass


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTExample(client))
