"""
This is (hopefully) a better, more stable version of YouTube notifications cog.
Previous version was on occasions spamming with pings, which is why it was disabled by default.
Assumed problem was ScrapeTube library that was used, that's why in this one there are no uncommon libraries used.
"""

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

        self.channels: list[dict[str, list[str] | str]] = []
        # format: [
        #   {
        #     "channelId": "ID",
        #     "latestVideos": ["videoId", "videoId", "videoId", "videoId", "videoId"]
        #   }
        # ]

        self.check.start()

    @tasks.loop(minutes=5)
    async def check(self):
        """ Checks every 5 minutes for a new video"""

        pass


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTYoutubeModule(client))
