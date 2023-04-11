import discord
from discord.ext import commands
from discord import app_commands
from cogs.LIBLocale import *


class EXTRoles(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        self.user_roles: dict[str, str] = {
            "role_name_stream_watcher": "user",
            "role_name_game_participant": "user",
            "role_name_event_member": "user",
            "role_name_logic_questions": "user"
        }
        self.loc = Localizer()

    @app_commands.command(name="role", description="grants/retrieves access to a certain role")
    async def role(self, interaction: discord.Interaction):
        self.loc.guild_id = interaction.guild_id        # I can't find how to fix this trash

        user_roles = interaction.user.roles
        select = discord.ui.Select(
            placeholder=self.loc.bw("role_cmd_placeholder"),
            row=1,
            min_values=1,
            max_values=4,
            options=[
                discord.SelectOption(
                    label=self.loc.bw("role_name_stream_watcher"),
                    description=self.loc.bw("role_desc_stream_watcher"),
                    emoji="✅" if discord.utils.get(user_roles,
                                                   name=self.loc.bw("role_name_stream_watcher")) else "❌"
                ),
                discord.SelectOption(
                    label=self.loc.bw("role_name_game_participant"),
                    description=self.loc.bw("role_desc_game_participant"),
                    emoji="✅" if discord.utils.get(user_roles,
                                                   name=self.loc.bw("role_name_game_participant")) else "❌"
                ),
                discord.SelectOption(
                    label=self.loc.bw("role_name_event_member"),
                    description=self.loc.bw("role_desc_event_member"),
                    emoji="✅" if discord.utils.get(user_roles,
                                                   name=self.loc.bw("role_name_event_member")) else "❌"
                ),
                discord.SelectOption(
                    label=self.loc.bw("role_name_logic_questions"),
                    description=self.loc.bw("role_desc_logic_questions"),
                    emoji="✅" if discord.utils.get(user_roles,
                                                   name=self.loc.bw("role_name_logic_questions")) else "❌"
                )
            ]
        )

        async def callback(inter: discord.Interaction):
            embed = discord.Embed(title=self.loc.bw("cmd_success"),
                                  description=self.loc.bw("role_cmd_role_change"),
                                  color=discord.Color.green())
            for role_name in select.values:
                role = discord.utils.get(inter.guild.roles, name=role_name)
                if role not in inter.user.roles:
                    embed.add_field(name=self.loc.bw("role_cmd_role_added"),
                                    value=role_name, inline=False)
                    await inter.user.add_roles(role)
                else:
                    embed.add_field(name=self.loc.bw("role_cmd_role_removed"),
                                    value=role_name, inline=False)
                    await inter.user.remove_roles(role)
            await inter.response.send_message(embed=embed, ephemeral=True)
            await interaction.delete_original_message()

        select.callback = callback
        view = discord.ui.View()
        view.add_item(select)

        await interaction.response.send_message(view=view, ephemeral=True)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTRoles(client))
