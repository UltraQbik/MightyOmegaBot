"""
This is (hopefully) a better, more stable version of YouTube notifications cog.
Previous version was on occasions spamming with pings, which is why it was disabled by default.
Assumed problem was ScrapeTube library that was used, that's why in this one there are no uncommon libraries used.
"""

import json
import configparser
from discord.ext import commands, tasks
from client_cogs.YTNotifications.fetcher import fetch_videos


class EXTYoutubeModule(commands.Cog):
    """
    This is YouTube notification cog. It will notify users for when a new video comes out,
    and put a notification about it to a designated channel. Edit `YTNotifications.cfg` to change the channel,
    and channels that it will be testing
    """

    def __init__(self, client: commands.Bot):
        self.client = client

        # cog's config file
        self.notifs_cfg: dict[int, dict[str, int | list[str]]] = {}
        # {
        #   [guildId]: {
        #     "newsChannel": [channelId],
        #     "channels": [[ytchannelId], [ytchannelId], [ytchannelId]]
        #   }
        # }

        # YouTube channel's list of 5 last videos
        self.channels: dict[str, list] = {}
        # {
        #   [ytchannelId]: [[videoId], [videoId], [videoId], [videoId], [videoId]]
        # }

        self.load_configs()
        # self.check.start()

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
                "channels": channels
            }
            channel_urls.update(channels)

        # update all channels
        for channel in channel_urls:
            self.channels[channel] = fetch_videos(channel, 5)

    @tasks.loop(minutes=5)
    async def check(self):
        """ Checks every 5 minutes for a new video"""

        pass


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTYoutubeModule(client))
