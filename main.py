import discord
from discord.ext import commands


class Client(commands.Bot):
    def __init__(self):
        super(Client, self).__init__(command_prefix=commands.when_mentioned_or("!"), intents=discord.Intents.all(),
                                     help_command=None)

        self.cog_list = [
            "cogs.EXTLoader",
            "cogs.EXTRoles",
            "cogs.EXTLogging"
        ]

    async def setup_hook(self) -> None:
        for ext in self.cog_list:
            await self.load_extension(ext)

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
                    print(f"\tAdded role to: {member.name} / {member.display_name}")
        print("Done!\n")

    @staticmethod
    async def on_member_join(member: discord.Member):
        role = discord.utils.get(member.guild.roles, name="∈")
        await member.add_roles(role)


def main():
    client = Client()
    with open("token.txt", "r") as f:
        tok = f.read()
    client.run(tok)


if __name__ == '__main__':
    main()

