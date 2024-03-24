import discord
from datetime import timedelta
from discord.ext import commands
from discord import app_commands


class EXTBetterTimeouts(commands.Cog):
    """
    Better timeout command cog
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="btimeout", description="timeouts a user")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.describe(
        user="User to timeout",
        seconds="how many seconds to timeout for",
        minutes="how many minutes to timeout for",
        hours="how many hours to timeout for",
        days="how many days to timeout for",
        weeks="how many weeks to timeout for",
        reason="reason for a timeout (default is 'bad behaviour')")
    async def btimeout(
            self,
            interaction: discord.Interaction,
            user: discord.Member,
            seconds: int = 60,
            minutes: int = 0,
            hours: int = 0,
            days: int = 0,
            weeks: int = 0,
            reason: str = "bad behaviour"
    ) -> None:
        """
        Command that will time you out
        """

        # calculate duration, and give a timeout
        duration = timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days, weeks=weeks)
        await user.timeout(duration, reason=reason)

        # make a pretty embed
        author_embed = discord.Embed(title="Success!", description=f"User {user.name} was put on a timeout",
                                     color=discord.Color.green())

        # send the pretty embed
        await interaction.response.send_message(embed=author_embed, ephemeral=True)

        # make a pretty embed
        user_embed = discord.Embed(title="Timeout!", description="You were put on a timeout",
                                   color=discord.Color.red())
        user_embed.add_field(name="Reason", value=reason, inline=True)
        user_embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

        # try to send user a dm with a reason for a timeout
        try:
            await user.send(embed=user_embed)

        # if it failed for these reasons, just ignore
        except discord.HTTPException or discord.Forbidden:
            pass

        # if something else failed, print a message
        except Exception as e:
            print(f"WARN: {e}; in BetterTimeouts cog")

    @btimeout.error
    async def btimeout_handle(self, interaction: discord.Interaction, error: discord.DiscordException):
        """
        Error handler for btimeout
        """

        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("User has more permissions than the bot", ephemeral=True)
        else:
            await interaction.response.send_message(str(error), ephemeral=True)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTBetterTimeouts(client))
