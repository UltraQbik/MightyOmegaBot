import os
import sys
import discord
import configparser
from discord.ext import commands


GLOBAL_CONFIG = {}


class Client(commands.Bot):
    def __init__(self):
        super(Client, self).__init__(command_prefix="!", intents=discord.Intents.all(),
                                     help_command=None)

        # make sure the var directory is present
        if not os.path.isdir("var"):
            os.mkdir("var")

        # list of all discord cogs
        # format: {"extension": "filepath"}
        self.working_extensions: dict[str, str] = {}

        # list of discord cogs that loaded by default
        # format: ["extension1", "extension2", ...]
        self.loaded_extensions: list[str] = [
            "Minesweeper_Game",
            "Help_Command",
            "Rofl_Commands",
            # "Youtube_Notifications",  # too unstable
            "LaTeX_Converter",
            "Remind_Me"
        ]

        # check all the installed extensions
        self.check_working_extensions()

    def check_working_extensions(self):
        for folder in os.listdir("client_cogs"):
            # check if main file exists
            if os.path.isfile(f"client_cogs/{folder}/main.py"):
                # import the extension to the list of working extensions
                # with the name being the name of the folder it's in
                self.working_extensions[folder] = f"client_cogs.{folder}.main"

    async def load_custom_extension(self, name):
        await self.load_extension(self.working_extensions[name])

    async def unload_custom_extension(self, name):
        await self.unload_extension(self.working_extensions[name])

    async def reload_custom_extension(self, name):
        await self.reload_extension(self.working_extensions[name])

    async def setup_hook(self) -> None:
        for ext in self.loaded_extensions:
            await self.load_custom_extension(ext)

    async def on_ready(self) -> None:
        print("\nBot started successfully!\n")
        await self.change_presence(activity=discord.Game("God Revision 2"))

        sync = await self.tree.sync()
        print(f"Slash command tree synced {len(sync)} commands\n")

        print("User membership test")
        for guild in self.guilds:
            try:
                role_id = int(GLOBAL_CONFIG["roles config"][guild.id.__str__()]["DiscordMemberRole"])
            except KeyError:
                print(f"\tGuild '{guild.name}' doesn't have roles configured", end="\n\n")
                continue
            for member in guild.members:
                # You are NOT supposed to do that, but we do NEED to check by role's id
                if role_id not in member._roles:
                    await member.add_roles(guild.get_role(role_id))
                    print(f"\tAdded role to: {member.id} / {member.display_name}")
        print("Done!\n")

    @staticmethod
    async def on_member_join(member: discord.Member):
        role_id = int(GLOBAL_CONFIG["roles config"][member.guild.id.__str__()]["DiscordMemberRole"])
        await member.add_roles(member.guild.get_role(role_id))


def parse_config_file(filepath: str):
    config = configparser.ConfigParser()
    config.read(filepath)
    return config


def main():
    # Useless message at the start of the bot
    if os.name != "nt":
        print("NOTE: You are running on non-windows machine, some of the things may be buggy\n"
              "Please report any issues on 'https://github.com/UltraQbik/MightyOmegaBot/issues'\n\n")

    # Load all configs from 'discord configs'
    global GLOBAL_CONFIG
    for file in os.listdir("client_configs"):
        if os.path.isfile(f"client_configs/{file}"):
            GLOBAL_CONFIG[os.path.splitext(file)[0]] = parse_config_file(f"client_configs/{file}")

    client = Client()
    client.run(sys.argv[1])


if __name__ == '__main__':
    main()
