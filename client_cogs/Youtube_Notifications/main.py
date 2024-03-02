import asyncio
import json
import scrapetube
import discord
from discord.ext import commands, tasks


def read_config() -> dict[int, dict[str, dict[str, str]]]:
    with open("client_cogs/Youtube_Notifications/config.json") as file:
        config = json.load(file)

    out_config = {}
    for channel_id in config:
        out_config[int(channel_id)] = config[channel_id]

    return out_config


class EXTYoutubeModule(commands.Cog):
    """
    Class that checks every minute for a new video.
    It has config in config.json, which looks something like this:
    {
        "discord_channel_id":
        {
            "Chanel_name":
            {
                "url": "URL to channel",
                "video": "Message with mention"
            }
        }
    }

    In "video" you can also use "{0}" (channel name) and "{1}" (video URL).
    """

    def __init__(self, client: commands.Bot):
        self.client = client

        self.config: dict[int, dict[str, dict[str, str]]] = read_config()
        self.videos: dict[int, dict[str, list[str]]] = {
            channel_id: {
                channel_name: [] for channel_name in self.config[channel_id]
            } for channel_id in self.config
        }

        self.discord_channels = []

        asyncio.get_running_loop().create_task(self.get_channels())

        self.check.start()

    async def get_channels(self):
        self.discord_channels = []
        for channel_id in self.config:
            try:
                self.discord_channels.append(
                    await self.client.fetch_channel(channel_id)
                )
            except discord.errors.Forbidden:
                print(f"Cannot get {channel_id} (Missing permissions)")
            except discord.errors.NotFound:
                print(f"Cannot get {channel_id} (Channel not found)")
            else:
                print(f"Added {channel_id}")


    @tasks.loop(minutes=1)
    async def check(self):
        """ Checks every minute for a new video """

        # Unnecessary; Update config every minute
        # self.config = read_config()

        for channel in self.discord_channels:
            if channel is None:
                print("Skipping some channel, because it's None.")
                continue
            for channel_name in self.config[channel.id]:
                videos = scrapetube.get_channel(
                    channel_url=self.config[channel.id][channel_name]["url"],
                    limit=5
                )
                try:
                    video_ids = [video["videoId"] for video in videos]
                except Exception as e:
                    print(f"Another BS error from somewhere: {e}")
                    continue

                if self.check.current_loop <= 1:
                    self.videos[channel.id][channel_name] = video_ids
                    continue

                for video_id in video_ids:
                    if video_id in self.videos[channel.id][channel_name]:
                        continue
                    url = f"https://youtu.be/{video_id}"

                    await channel.send(
                        self.config[channel.id][channel_name]["video"].format(
                            channel_name, url
                        )
                    )
                self.videos[channel.id][channel_name] = video_ids


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTYoutubeModule(client))
