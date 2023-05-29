import discord
from discord.ext import commands
from discord import app_commands
from minesweeper.field import Field


class EXTMinesweeper(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands
    @app_commands.command(
        name="ms-gen",
        description="Generates minesweeper field")
    async def ms_gen(self, interaction: discord.Interaction):
        generated_field = Field(10, 9).generate()
        await interaction.response.send_message(str(generated_field))


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTMinesweeper(client))
