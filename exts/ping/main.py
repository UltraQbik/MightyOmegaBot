import discord
from discord.ext import commands
from discord import app_commands


class EXTPing(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="ping", description="pong!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Pong {interaction.user.mention}! {self.client.latency * 1000:.2f} ms")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTPing(client))
