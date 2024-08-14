"""
This is a status slash command cog.
Prints out a status of certain things you choose
"""


import psutil
import discord
from datetime import datetime
from discord import app_commands
from discord.ext import commands


class EXTStatus(commands.Cog):
    """
    Status command cog
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

        # time when the cog was added
        # generally is the starting time of the bot
        self.start_time: datetime = datetime.now()

    @app_commands.command(name="status", description="returns status")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Bot", value="bot"),
        app_commands.Choice(name="Host", value="host"),
        app_commands.Choice(name="Minecraft", value="mc")
    ])
    async def status(
        self,
        interaction: discord.Interaction,
        choices: app_commands.Choice[str]
    ) -> None:
        """
        This is an example slash command
        """

        if choices.value == "bot":
            ping = self.client.latency

            # uptime stuff
            uptime = (datetime.now() - self.start_time).total_seconds()
            minutes = uptime / 60
            hours = minutes / 60
            days = hours / 24
            weeks = days / 7
            months = days / 30

            uptime_str = ""
            if int(uptime) % 60 > 0:
                uptime_str = f"{int(uptime) % 60} second{'' if int(uptime) % 60 == 1 else 's'}"
            if int(minutes) % 60 > 0:
                uptime_str = f"{int(minutes) % 60} minute{'' if int(minutes) % 60 == 1 else 's'} " + uptime_str
            if int(hours) % 24 > 0:
                uptime_str = f"{int(hours) % 24} hour{'' if int(hours) % 24 == 1 else 's'} " + uptime_str
            if int(days) % 60 > 0:
                uptime_str = f"{int(days) % 7} day{'' if int(days) % 7 == 1 else 's'} " + uptime_str
            if int(weeks) % 4.28 > 0:
                uptime_str = f"{int(weeks) % 4.28} week{'' if int(weeks) % 4.28 == 1 else 's'} " + uptime_str
            if int(months) > 0:
                uptime_str = f"{int(months)} month{'' if int(months) == 1 else 's'} " + uptime_str

            embed = discord.Embed(title="Bot status", description="Current bot status",
                                  color=discord.Color.green())
            embed.add_field(name="latency", value=f"{ping*1000:.2f} ms", inline=False)
            embed.add_field(name="uptime", value=uptime_str, inline=False)

            await interaction.response.send_message(embed=embed)
        elif choices.value == "host":
            pass
        else:
            pass

async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTStatus(client))
