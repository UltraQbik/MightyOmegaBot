import discord
from discord.ext import commands
from discord import app_commands
import pnglatex


class EXTHelpcmd(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="latex", description="converts LaTeX to image")
    @app_commands.describe(text="LaTeX formatted text")
    async def help_cmd(self, text: str, interaction: discord.Interaction):
        try:
            pnglatex.pnglatex(text, "image.png")
        except ValueError as exc:
            await interaction.response.send_message(
                str(exc),
                ephemeral=True
            )
        else:
            with open("image.png", "rb") as f:
                await interaction.response.send_message(
                    file=discord.File(f)
                )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTHelpcmd(client))
