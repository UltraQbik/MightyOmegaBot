"""
This is an example extension cog for MightyOmegaBot.
It shows you how to add your own cogs for the bot if you want to contribute.
"""
import json
import os
import discord
from discord import app_commands
from discord.ext import commands


class EXTLogger(commands.Cog):
    """
    This is an example cog which adds example commands
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

        # path to logger's database
        self.db_path = "var/logger_db.json"
        if not os.path.isfile(self.db_path):
            with open(self.db_path, "w", encoding="utf8") as file:
                file.write("[\n]")

        # read the database
        self.db: list[dict[str, str]] | None = None
        with open(self.db_path, "r", encoding="utf8") as file:
            try:
                self.db = json.loads(file.read())
            except json.decoder.JSONDecodeError:
                print("WARN: Logger unable to load the database due to json decoder error")
                print("WARN: Logger cog is down")
                self.cog_unload()
                return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """
        When the message is edited
        """

        pass

    def update_database(self):
        """
        Updates logger's database
        """

        # check that the database file is in its place still
        # may not be necessary, but it's here anyway
        if not os.path.isfile(self.db_path):
            print("WARN: Loggers database was removed while the bot was running.")
            print("INFO: Loggers database will be created from the one currently loaded")

        # write updates to the database file
        with open(self.db_path, "w", encoding="utf8") as file:
            file.write(json.dumps(self.db, indent=2))


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTLogger(client))
