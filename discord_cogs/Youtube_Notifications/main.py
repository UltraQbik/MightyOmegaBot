import scrapetube
from discord.ext import commands, tasks


def get_yt_channels() -> dict[str, str]:
    with open("discord_cogs/Youtube_Notifications/channels.txt", "r") as file:
        channel_list = file.read().replace("\r\n", "\n").split("\n")
        channels = {}
        for entry in channel_list:
            if not entry:
                continue
            channel_name, channel_url = entry.split(" ")
            channels[channel_name] = channel_url
    return channels


class EXTYoutubeModule(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        self.channels: dict[str, str] = get_yt_channels()
        self.videos: dict[str, list[str]] = {}

    @tasks.loop(minutes=1)
    async def check(self):
        """ Checks every minute for a new video, from channels in 'channels.txt' """

        # Unnecessary; Update channel list every minute
        # self.channels = get_yt_channels()
        discord_channel = self.client.get_channel(863394227655933994)

        for channel_name, channel_url in self.channels:
            videos = scrapetube.get_channel(channel_url=channel_url, limit=5)
            video_ids = [video["videoId"] for video in videos]

            if self.check.current_loop == 0:
                self.videos[channel_name] = video_ids
                continue

            for video_id in video_ids:
                if video_id not in self.videos[channel_name]:
                    url = f"https://youtu.be/{video_id}"

                    # ye, roles are not fully supported just yet
                    await discord_channel.send(
                        f"<@&1101231667554828410><@&1110299526721449984>\n"
                        f"\n"
                        f"# :fire: Новое видео на канале {channel_name}! :fire:\n"
                        f"# [Ссылочка в сибирь :>]({url})"
                    )

            self.videos[channel_name] = video_ids


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTYoutubeModule(client))
