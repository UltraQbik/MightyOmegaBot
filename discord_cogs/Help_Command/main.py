import discord
from discord.ext import commands
from discord import app_commands


class EXTHelpcmd(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="help", description="gives the list of commands!")
    async def help_cmd(self, interaction: discord.Interaction):
        help_list = ""

        # Walks through the list of slash commands
        for cmd in self.client.tree.walk_commands():
            help_list += f"- **/{cmd.name}** - {cmd.description}\n"

        # Goes through the list of '!' commands
        for cmd in self.client.commands:
            help_list += f"- **!{cmd.name}** - {cmd.description}\n"

        await interaction.response.send_message(help_list)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTHelpcmd(client))
