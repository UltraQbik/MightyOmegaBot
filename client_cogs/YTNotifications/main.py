"""
This is (hopefully) a better, more stable version of YouTube notifications cog.
Previous version was on occasions spamming with pings, which is why it was disabled by default.
Assumed problem was ScrapeTube library that was used, that's why in this one there are no uncommon libraries used.
"""

import json
import configparser
from discord.ext import commands, tasks
from client_cogs.YTNotifications.fetcher import fetch_videos, fetch_channel_name


class EXTYoutubeModule(commands.Cog):
    """
    This is YouTube notification cog. It will notify users for when a new video comes out,
    and put a notification about it to a designated channel. Edit `YTNotifications.cfg` to change the channel,
    and channels that it will be testing
    """

    def __init__(self, client: commands.Bot):
        self.client = client

        # cog's config file
        self.notifs_cfg: dict[int, dict[str, str | int | list[str]]] = {}
        # {
        #   [guildId]: {
        #     "newsChannel": [channelId],
        #     "pingRole": [roleId],
        #     "pingMsg": [string],
        #     "channels": [[ytchannelId], [ytchannelId], [ytchannelId]]
        #   }
        # }

        # YouTube channel's list of 5 last videos
        self.channels: dict[str, list] = {}
        # {
        #   [ytchannelId]: [[videoId], [videoId], [videoId], [videoId], [videoId]]
        # }

        self.load_configs()
        self.check.start()

    def load_configs(self):
        """
        Loads configs into the cog
        """

        # read the config files
        cfg = configparser.ConfigParser()
        cfg.read("client_configs/YTNotifications.cfg")

        # keep track of channel urls
        channel_urls: set[str] = set()

        # write config into ram
        for guild_id in cfg.sections():
            channels = json.loads(cfg[guild_id]["channels"])
            self.notifs_cfg[int(guild_id)] = {
                "newsChannel": int(cfg[guild_id]["newsChannel"]),
                "pingRole": int(cfg[guild_id]["pingRole"]),
                "pingMsg": cfg[guild_id]["pingMsg"],
                "channels": channels
            }
            channel_urls.update(channels)

        # update all channels
        for channel in channel_urls:
            self.channels[channel] = fetch_videos(channel, 5)

    @tasks.loop(minutes=5)
    async def check(self):
        """ Checks every 5 minutes for a new video"""

        # go through all guilds the bot is in
        for guild in self.client.guilds:

            # skip guild, if it's not in notifications config
            if guild.id not in self.notifs_cfg:
                continue

            news_channel = self.client.get_channel(self.notifs_cfg[guild.id]["newsChannel"])

            # skip if something wasn't configured properly
            # and print a message
            if news_channel is None:
                print("WARN: YTNotifs: news channel is not configured properly")
                continue

            # go through channels, and check for new videos
            for channel in self.notifs_cfg[guild.id]["channels"]:
                # fetch 5 last videos
                last_videos = fetch_videos(channel, 5)

                # go through videos, and check if they are all in the database
                for video in last_videos:
                    # if video is not in the database, make a notification about it
                    if video not in self.channels[channel]:
                        message = self.notifs_cfg[guild.id]["pingMsg"]
                        message = message.format(
                            ping=f'<@&{self.notifs_cfg[guild.id]["pingRole"]}>',
                            channel_name=fetch_channel_name(channel),
                            video_link=f'https://www.youtube.com/watch?v={video}'
                        )

                        await news_channel.send(message)

                # update the database
                self.channels[channel] = last_videos


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTYoutubeModule(client))
