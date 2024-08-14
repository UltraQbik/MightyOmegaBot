"""
This is a status slash command cog.
Prints out a status of certain things you choose
"""


import psutil
import discord
from discord import app_commands
from discord.ext import commands


class EXTStatus(commands.Cog):
    """
    Status command cog
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

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

        await interaction.response.send_message(choices.value)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTStatus(client))
