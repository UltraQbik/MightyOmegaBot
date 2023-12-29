import scrapetube
import clientconfig
import configparser
from discord.ext import commands, tasks


class EXTYoutubeModule(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        self.config: None | dict[str, configparser.ConfigParser] = clientconfig.get_config()
        self.channels: dict[str, list] = {}
        self.videos: dict[str, list[str]] = {}

        self.check.start()

    @staticmethod
    def parse_channel_list(channel_list: str):
        # list looks like this
        # [NAME] [URL],[NAME] [URL],[NAME] [URL],...
        # split by ',' to get list of '[NAME] [URL]'
        # split sub-lists by ' ' to get individual names and urls of channels

        parsed = []
        list_ = channel_list.split(",")
        for item in list_:
            channel = item.split(" ")
            parsed.append({"name": channel[0], "url": channel[1]})
        return parsed

    @tasks.loop(minutes=1)
    async def check(self):
        for guild in self.client.guilds:
            # fetch news channel
            guild_config = self.config["youtube"][guild.id.__str__()]
            if self.check.current_loop == 1:
                self.channels[guild.id.__str__()] = self.parse_channel_list(guild_config["NotificationChannelList"])

            discord_channel = self.client.get_channel(int(guild_config["NotificationNewsChannel"]))

            # go through all listed to check channels
            for channel in self.channels[guild.id.__str__()]:
                # get their videos
                videos = scrapetube.get_channel(channel_url=channel["url"], limit=5)
                video_ids = [video["videoId"] for video in videos]

                # if the module was just activated
                if self.check.current_loop == 1:
                    self.videos[channel["url"]] = video_ids
                    continue

                # go through videos, and post new ones
                for video_id in video_ids:
                    if video_id not in self.videos[channel["url"]]:
                        url = f"https://youtu.be/{video_id}"

                        pings = "".join([f"<@&{pid}>" for pid in guild_config["NotificationRoles"].split(",")])
                        await discord_channel.send(
                            guild_config["NotificationNewsMessage"].replace("\\n", "\n").format(
                                ping=pings, name=channel["name"], url=url)
                        )

                self.videos[channel["url"]] = video_ids


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTYoutubeModule(client))
