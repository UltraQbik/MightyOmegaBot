import discord
from discord.ext import commands
from discord import app_commands
import sympy
from PIL import Image, ImageOps


class EXTLatexConverter(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="latex", description="converts LaTeX to image")
    @app_commands.describe(text="LaTeX formatted text")
    async def latex_cmd(self, interaction: discord.Interaction, text: str):
        try:
            sympy.preview(
                f"$${text}$$",
                output="png",
                viewer="file",
                filename="image.png",
                euler=False,
                dvioptions=['-D', '400']
            )
        except RuntimeError as exc:
            text = str(exc).replace('\\n', '\n')
            out = text[text.find('! '):]
            out = out[:out.find('\n')]
            await interaction.response.send_message(
                out,
                ephemeral=True
            )
        else:
            with Image.open("image.png") as img:
                img_borders = ImageOps.expand(
                    img,
                    border=20,
                    fill='white'
                )
                img_borders.save("image.png")
            with open("image.png", "rb") as f:
                await interaction.response.send_message(
                    file=discord.File(f)
                )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTLatexConverter(client))
