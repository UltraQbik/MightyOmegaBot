import discord
from discord.ext import commands
from discord import app_commands
from exts.minesweeper.field import Field


class EXTSnake(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name="snake",
        description="Play snake")
    async def snake(
        self,
        interaction: discord.Interaction,
    ) -> None:
        await interaction.response.send_message("TODO: Create snake")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTSnake(client))

