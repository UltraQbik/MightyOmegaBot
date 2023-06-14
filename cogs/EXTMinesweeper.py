import discord
from discord.ext import commands
from discord import app_commands
from minesweeper.field import Field


class EXTMinesweeper(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name="ms-gen",
        description="Generates minesweeper field")
    @app_commands.describe(
        size="Size of the field (default: 9)",
        mines="Number of mines on the field (default: 10)")
    async def ms_gen(
        self,
        interaction: discord.Interaction,
        size: int = 9,
        mines: int = 10
    ):
        field = Field(size, mines)
        field.generate()
        await interaction.response.send_message(f"Minesweeper\n{field}")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTMinesweeper(client))
