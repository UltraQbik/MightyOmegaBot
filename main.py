import os
import sys
import discord
from discord.ext import commands
from discord import app_commands
# from configparser import ConfigParser


class Client(commands.Bot):
    def __init__(self):
        super(Client, self).__init__(command_prefix=None, intents=discord.Intents.all(),
                                     help_command=None)

        # stores of list of all exts
        # format: {"extension": "filepath"}
        self.working_extensions: dict[str, str] = {}

        # stores the list of exts loaded by default
        # format: ["extension1", "extension2", ...]
        self.loaded_extensions: list[str] = ["minesweeper", "ping"]

        # check all the installed extensions
        self.check_working_extensions()

    def check_working_extensions(self):
        for folder in os.listdir("exts"):
            # check if 'main.py' exists
            if os.path.isfile(f"exts/{folder}/main.py"):
                # import the extension to the list of working extensions
                # with the name being the name of the folder it's in
                self.working_extensions[folder] = f"exts.{folder}.main"

            # NOTE: This is a bit way too over-engineered
            # if os.path.isfile(f"exts/{folder}/extension.cfg"):
            #     # read the config file
            #     config = ConfigParser()
            #     config.read(f"exts/{folder}/extension.cfg")
            #
            #     # check if config contains the extension name
            #     if config.has_section("DEFAULT") and config["DEFAULT"].get("ExtensionName") is not None \
            #        and os.path.isfile(f"exts/{folder}/main.py"):
            #         # write it to the list of working extensions
            #         self.working_extensions[config["DEFAULT"]["ExtensionName"]] = f"exts.{folder}.main.py"

    async def load_custom_extension(self, name):
        await self.load_extension(self.working_extensions[name])

    async def unload_custom_extension(self, name):
        await self.unload_extension(self.working_extensions[name])

    async def reload_custom_extension(self, name):
        await self.reload_extension(self.working_extensions[name])

    async def setup_hook(self) -> None:
        for ext in self.loaded_extensions:
            await self.load_custom_extension(ext)

    # this function is from an old code, and should be changed later to add support for custom member roles
    async def on_ready(self) -> None:
        print("\nBot started successfully!\n")
        await self.change_presence(activity=discord.Game("god"))

        sync = await self.tree.sync()
        print(f"Slash command tree synced {len(sync)} commands\n")

        print("User membership test")
        for guild in self.guilds:
            role = discord.utils.get(guild.roles, name="∈")
            for member in guild.members:
                if role not in member.roles:
                    await member.add_roles(role)
                    print(f"\tAdded role to: {member.id} / {member.display_name}")
        print("Done!\n")

    # same thing as for the 'on_ready' function
    @staticmethod
    async def on_member_join(member: discord.Member):
        role = discord.utils.get(member.guild.roles, name="∈")
        await member.add_roles(role)


def main():
    client = Client()
    client.run(sys.argv[1])


if __name__ == '__main__':
    main()