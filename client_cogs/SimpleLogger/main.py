"""
This is an example extension cog for MightyOmegaBot.
It shows you how to add your own cogs for the bot if you want to contribute.
"""

import discord
import configparser
from discord.ext import commands


class EXTLogger(commands.Cog):
    """
    This is an example cog which adds example commands
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

        # cog's configs
        # format: {"[guild_id]": channel}
        self.logging_cfg: dict[int, int] = {}

        # load configs
        self.load_configs()

    def load_configs(self):
        """
        Loads cog's configs
        """

        cfg = configparser.ConfigParser()
        cfg.read("client_configs/SimpleLogger.cfg")

        for guild_id in cfg.sections():
            self.logging_cfg[int(guild_id)] = int(cfg[guild_id]["loggingChannel"])

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """
        When the message is edited
        """

        # do something

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """
        When the message is deleted
        """

        # check if logger was configured
        if message.guild.id not in self.logging_cfg:
            print("ERROR: SimpleLogger: cog was not configured properly")
            return

        # fetch logging channel
        channel = self.client.get_channel(self.logging_cfg[message.guild.id])

        # make a pretty embed
        embed = discord.Embed(
            title="Delete message",
            description=f"Channel: {channel.name}",
            color=discord.Color.red())
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
        embed.add_field(name="Created at:", value=f"<t:{message.created_at.timestamp():.0f}>", inline=False)
        embed.add_field(name="Content:", value=message.content, inline=False)

        # send the embed
        await channel.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTLogger(client))
