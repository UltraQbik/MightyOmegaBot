"""
This is SimpleLogger cog for the MightyOmegaBot. It does what it says, and it just logs the messages of the users.
Notification about any message that was deleted / edited will be sent to a designated by user channel.

To add channel for notifications edit `SimpleLogger.cfg` file, and add following lines
```
[guild_id]
loggingChannel=[channel_id]
```
"""

import discord
import configparser
from discord.ext import commands


class EXTLogger(commands.Cog):
    """
    This is simple logger cog. It will log when users edit / delete messages,
    and put a notification about it to a designated channel. Edit `SimpleLogger.cfg` to change the channel
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

        # check if logger was configured
        if after.guild.id not in self.logging_cfg:
            print("ERROR: SimpleLogger: cog was not configured properly")
            return

        # fetch logging channel
        channel = self.client.get_channel(self.logging_cfg[after.guild.id])

        # make a pretty embed
        embed = discord.Embed(
            title="Edited message",
            description=f"Channel: {after.channel.name}",
            color=discord.Color.orange())
        embed.set_author(name=after.author.display_name, icon_url=after.author.avatar.url)
        embed.add_field(name="Created at:", value=f"<t:{after.created_at.timestamp():.0f}>", inline=False)
        embed.add_field(name="Edited at:", value=f"<t:{after.edited_at.timestamp():.0f}>", inline=False)
        embed.add_field(name="Content before:",
                        value=before.content if len(before.content) < 1024 else before.content[:1018] + '...',
                        inline=False)
        embed.add_field(name="Content after:",
                        value=after.content if len(after.content) < 1024 else after.content[:1018] + '...',
                        inline=False)

        # send the embed
        await channel.send(embed=embed)

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
            description=f"Channel: {message.channel.name}",
            color=discord.Color.red())
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
        embed.add_field(name="Created at:", value=f"<t:{message.created_at.timestamp():.0f}>", inline=False)
        embed.add_field(name="Content:",
                        value=message.content if len(message.content) < 1024 else message.content[:1018] + '...',
                        inline=False)

        # send the embed
        await channel.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTLogger(client))
