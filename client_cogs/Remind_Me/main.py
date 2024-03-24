"""
The extension to 'NotABot' discord not a bot client [https://github.com/nakidai/NotABot],
which adds '/remindme' command, which then was added to MightyOmegaBot (with some slight changes)
"""


import os
import json
import discord
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from discord import app_commands


# Constants
DATABASE_UPDATE_TIME: int = 5       # in seconds
PER_USER_REMINDER_LIMIT: int = 30   # how many reminders can 1 user have


class EXTRemindMe(commands.Cog):
    """
    This is the 'remind me' command cog
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

        # make sure that the database file exists
        # if an outage happens, the bot will still save the messages.
        self.db_path: str = "var/remindme_db.json"
        if not os.path.isfile(self.db_path):
            with open(self.db_path, "w", encoding="utf8") as file:
                file.write("{\n}")

        # read the database
        with open(self.db_path, "r") as file:
            try:
                self.remindme_database: dict[str, list[dict[str, str]]] = json.loads(file.read())
            except json.decoder.JSONDecodeError:
                print("WARN: RemindMe Unable to load the database, due to an error when decoding it")
                print("WARN: RemindMe cog is down")
                self.cog_unload()
                return

        # start checking reminders
        self.check_reminders.start()

    @app_commands.command(name="remindme", description="Reminds you")
    @app_commands.describe(
        message="Message that needs to be reminded",
        minutes="In how many minutes to send a reminder (default is 1 minute)",
        hours="In how many hours to send a reminder",
        days="In how many days to send a reminder",
        weeks="In how many weeks to send a reminder",
        months="In how many months to send a reminder",
        years="In how many years to send a reminder")
    async def remindme(
        self,
        interaction: discord.Interaction,
        message: str,
        minutes: int = 1,
        hours: int = 0,
        days: int = 0,
        weeks: int = 0,
        months: int = 0,
        years: int = 0
    ) -> None:
        """
        This is the 'remind me' command implementation
        """

        # timedelta
        timed = timedelta(
            minutes=minutes,
            hours=hours,
            days=days + (months * 30.436875) + (years * 365.2422),
            weeks=weeks
        )

        # if the total amount of time is bigger than 10 years, give an error and die
        if timed.days > 3652:
            await interaction.response.send_message("I doubt the discord will exist for 10+ years.", ephemeral=True)
            return

        # if the total amount of seconds is 0, then give an error and *die*
        if timed.total_seconds() == 0:
            await interaction.response.send_message(f"To use instant reminders buy a DLC for 49.99$", ephemeral=True)
            return

        # check if user is already present
        if (user_id := str(interaction.user.id)) in self.remindme_database:
            # if so, check if the user didn't hit the "remindme" cap
            if len(self.remindme_database[user_id]) > PER_USER_REMINDER_LIMIT:
                await interaction.response.send_message(
                    f"You've reached the reminder limit of {PER_USER_REMINDER_LIMIT}", ephemeral=True)
                return

        # if not, add a list for them
        else:
            self.remindme_database[user_id] = []

        # add a reminder for a user
        future_time = datetime.now() + timed
        self.remindme_database[user_id].append({
            "timestamp": future_time.strftime("%Y-%m-%d %H:%M:%S"),
            "message": message
        })

        # send the sucks ass message
        await interaction.response.send_message("Reminder successfully created!")

        # update the database
        self.update_remindme_database()

    @tasks.loop(seconds=DATABASE_UPDATE_TIME)
    async def check_reminders(self):
        """
        A periodic check of reminders.
        """

        # go through the database
        for user_id, reminders in self.remindme_database.items():
            # fetch the user
            user = self.client.get_user(int(user_id))

            # go through the user's reminders
            reminder_idx = 0
            while reminder_idx < len(reminders):
                # fetch the reminder
                reminder = reminders[reminder_idx]

                # decode the stored timestamp
                timestamp = datetime.strptime(reminder["timestamp"], "%Y-%m-%d %H:%M:%S")

                # if the time is negative, that means it has already past that
                if (timestamp - datetime.now()).total_seconds() <= 0:
                    message = f"Reminder for <t:{int(timestamp.timestamp())}>\n{reminder['message']}"

                    # check that the message isn't too big
                    if len(message) >= 2000:
                        message = message[:1995] + "..."

                    # remove the reminder from the database
                    self.remindme_database[user_id].pop(reminder_idx)
                    reminder_idx -= 1

                    # try to send the reminder to the user's dm
                    try:
                        await user.send(message)

                    # if failed for these reasons, just ignore
                    except discord.HTTPException or discord.Forbidden:
                        pass

                    # if something else failed, put it in logs
                    except Exception as e:
                        print(f"WARN: {e}; in RemindMe cog")

                # increment the index
                reminder_idx += 1

        # update the database
        self.update_remindme_database()

    def update_remindme_database(self):
        """
        Updates the remindme user database
        """

        # check that the database file is in its place still
        # may not be necessary, but it's here anyway
        if not os.path.isfile(self.db_path):
            print("WARN: RemindMe database was removed while the bot was running.")
            print("INFO: RemindMe database will be created from the one currently loaded")

        # write updates to the database file
        with open(self.db_path, "w", encoding="utf8") as file:
            file.write(json.dumps(self.remindme_database, indent=2))


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTRemindMe(client))
