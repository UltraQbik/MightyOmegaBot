import discord
from discord.ext import commands
from discord import app_commands
from client_cogs.MinesweeperGame.field import Field


class EXTMinesweeper(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name="ms-gen",
        description="Generates minesweeper field")
    @app_commands.describe(
        size="Size of the field ((0, 10)) (default: 9)",
        mines="Number of mines on the field ((0, size^2]) (default: 10)")
    async def ms_gen(
        self,
        interaction: discord.Interaction,
        size: int = 9,
        mines: int = 10
    ):
        if size >= 10 or size <= 0 or mines <= 0 or mines > size**2:
            await interaction.response.send_message(
                "Incorrect values",
                ephemeral=True
            )
            return
        field = Field(size, mines)
        field.generate()
        await interaction.response.send_message(f"Minesweeper\n{field}")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTMinesweeper(client))
