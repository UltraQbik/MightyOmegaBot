"""
This is an example extension cog for MightyOmegaBot.
It shows you how to add your own cogs for the bot if you want to contribute.
"""

import json
import os
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands, tasks


class EXTLogger(commands.Cog):
    """
    This is an example cog which adds example commands
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

        # path to logger's database
        # every line is json, but the file itself is not
        self.db_path = "var/logger_db.json"
        if not os.path.isfile(self.db_path):
            open(self.db_path, "w", encoding="utf8").close()

        # launch the task
        self.check_database.start()

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """
        When the message is edited
        """

        # find references of same message id
        with open(self.db_path, "r+", encoding="utf8") as file:
            seek = 0
            while (line := file.readline()) is not None:
                # if we reached the end
                if line == "\n" or line == "":
                    break

                # decode the entry
                decoded_json = json.loads(line)

                # when the same message id is found, then append the changes to the entry and return
                if decoded_json["action"] == "edited" and decoded_json["message_id"] == str(before.id):
                    # append new edit
                    decoded_json["messages"].append(
                        {
                            "action_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "message": after.content
                        }
                    )
                    # update action time
                    decoded_json["action_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # seek to the beginning of the line
                    file.seek(seek, 0)

                    # write changes to the database
                    file.write(json.dumps(decoded_json) + "\n")
                    return

                # get the end of the line (beginning of next one)
                seek = file.tell()

        # if message doesn't already exist, add a new entry
        self.update_database(
            {
                "action": "edited",
                "action_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "creation_time": before.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "message_id": before.id.__str__(),
                "message_author_id": before.author.id,
                "message_author_dn": before.author.display_name,
                "messages": [
                    {
                        "action_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "message": before.content
                    },
                    {
                        "action_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "message": after.content
                    }
                ]
            }
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """
        When the message is deleted
        """

        # append data to the database
        self.update_database(
            {
                "action": "deleted",
                "action_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "creation_time": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "message_id": message.id.__str__(),
                "message_author_id": message.author.id,
                "message_author_dn": message.author.display_name,
                "message": message.content
            }
        )

    @tasks.loop(hours=4)
    async def check_database(self):
        """
        Checks logger's database and removes logs that are older than 1 day
        """

        # makes new temp database file with old record (older than 1 day) being deleted
        with open(self.db_path, "r", encoding="utf8") as file:
            with open(self.db_path + ".tmp", "w", encoding="utf8") as newfile:
                while (line := file.readline()) is not None:
                    # if we reached the end
                    if line == "\n" or line == "":
                        break

                    # fetch and decode entry
                    decoded_json = json.loads(line)

                    # if the entry is younger than 1 day, write to new file
                    time = datetime.strptime(decoded_json["action_time"], "%Y-%m-%d %H:%M:%S")
                    if (datetime.now() - time).total_seconds() < 86400:
                        newfile.write(line)

        # use os to delete old database, and rename new one
        os.remove(self.db_path)
        os.rename(self.db_path + ".tmp", self.db_path)

    def update_database(self, data: object):
        """
        Updates logger's database
        """

        # check that the database file is in its place still
        # may not be necessary, but it's here anyway
        if not os.path.isfile(self.db_path):
            print("WARN: Loggers database was removed while the bot was running.")
            print("INFO: Loggers database will be created from the one currently loaded")

        # write updates to the database file
        with open(self.db_path, "a", encoding="utf8") as file:
            file.write(json.dumps(data) + "\n")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTLogger(client))
