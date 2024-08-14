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

        match choices.value:
            case "bot":
                ping = self.client.latency

                # uptime stuff
                uptime = (datetime.now() - self.start_time).total_seconds()
                minutes = uptime / 60
                hours = minutes / 60
                days = hours / 24
                weeks = days / 7
                months = days / 30

                uptime_str = ""
                if int(uptime % 60) > 0:
                    uptime_str = f"{uptime % 60:.0f} second{'' if int(uptime % 60) == 1 else 's'}"
                if int(minutes % 60) > 0:
                    uptime_str = f"{minutes % 60:.0f} minute{'' if int(minutes % 60) == 1 else 's'} " + uptime_str
                if int(hours % 24) > 0:
                    uptime_str = f"{hours % 24:.0f} hour{'' if int(hours % 24) == 1 else 's'} " + uptime_str
                if int(days % 60) > 0:
                    uptime_str = f"{days % 7:.0f} day{'' if int(days % 7) == 1 else 's'} " + uptime_str
                if int(weeks % 4.28) > 0:
                    uptime_str = f"{weeks % 4.28:.0f} week{'' if int(weeks % 4.28) == 1 else 's'} " + uptime_str
                if int(months % 12) > 0:
                    uptime_str = f"{months % 4.28:.0f} month{'' if int(months % 4.28) == 1 else 's'} " + uptime_str

                embed = discord.Embed(title="Bot status", description="Current bot status",
                                      color=discord.Color.green())
                embed.add_field(name="latency", value=f"{ping*1000:.2f} ms", inline=False)
                embed.add_field(name="uptime", value=uptime_str, inline=False)

                await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTStatus(client))
