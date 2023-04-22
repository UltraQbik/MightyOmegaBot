import os
import discord
from discord.ext import commands


def is_owner():
    async def predicate(ctx):
        return ctx.author == ctx.guild.owner
    return commands.check(predicate)


class EXTLoader(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        aliases=["ledc"],
        name="loaded_cogs",
        description="list of loaded extensions")
    @is_owner()
    async def loaded_cogs(self, ctx):
        message = ""
        for idx, cog in enumerate(self.client.cogs, 1):
            message += f"[ {idx: >3} ] {cog}"
        await ctx.send(message)

    @commands.command(
        aliases=["available_cogs", "allc"],
        name="all_cogs",
        description="list of all extensions")
    @is_owner()
    async def all_cogs(self, ctx):
        message = ""
        for idx, cog in enumerate(os.listdir("cogs"), 1):
            if cog[0:3] == "EXT":
                message += f"[ {idx: >3} ] {os.path.splitext(cog)[0]}"
        await ctx.send(message)

    @commands.command(
        aliases=["lc"],
        name="load_cog",
        description="loads the extension")
    @is_owner()
    async def load_cog(self, ctx, cog_name: str):
        try:
            await self.client.load_extension("cogs." + cog_name)
            sync = await self.client.tree.sync()
            print(f"\nSlash command tree synced {len(sync)} commands\n")

            embed = discord.Embed(title="Success!",
                                  description=f"Successfully loaded '`{cog_name}`'!",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
        except commands.ExtensionError as e:
            embed = discord.Embed(title="Fail!",
                                  description=f"Unable to load '`{cog_name}`'!",
                                  color=discord.Color.red())
            embed.add_field(name="Exception:", value=str(e))
            await ctx.send(embed=embed)

    @commands.command(
        aliases=["uload_cog", "ulc"],
        name="unload_cog",
        description="unloads the extension")
    @is_owner()
    async def unload_cog(self, ctx, cog_name: str):
        try:
            await self.client.unload_extension("cogs." + cog_name)
            sync = await self.client.tree.sync()
            print(f"\nSlash command tree synced {len(sync)} commands\n")

            embed = discord.Embed(title="Success!",
                                  description=f"Successfully unloaded '`{cog_name}`'!",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
        except commands.ExtensionError as e:
            embed = discord.Embed(title="Fail!",
                                  description=f"Unable to unload '`{cog_name}`'!",
                                  color=discord.Color.red())
            embed.add_field(name="Exception:", value=str(e))
            await ctx.send(embed=embed)

    @commands.command(
        aliases=["rload_cog", "rlc"],
        name="reload_cog",
        description="reloads the extension")
    @is_owner()
    async def reload_cog(self, ctx, cog_name: str):
        try:
            await self.client.reload_extension("cogs." + cog_name)
            sync = await self.client.tree.sync()
            print(f"\nSlash command tree synced {len(sync)} commands\n")

            embed = discord.Embed(title="Success!",
                                  description=f"Successfully reloaded '`{cog_name}`'!",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
        except commands.ExtensionError as e:
            embed = discord.Embed(title="Fail!",
                                  description=f"Unable to reload '`{cog_name}`'!",
                                  color=discord.Color.red())
            embed.add_field(name="Exception:", value=str(e))
            await ctx.send(embed=embed)

    @load_cog.error
    async def load_error(self, ctx, error):
        embed = discord.Embed(title="Fail!",
                              description="You are not allowed to use that command!",
                              color=discord.Color.red())
        await ctx.send(embed=embed)

    @unload_cog.error
    async def unload_error(self, ctx, error):
        embed = discord.Embed(title="Fail!",
                              description="You are not allowed to use that command!",
                              color=discord.Color.red())
        await ctx.send(embed=embed)

    @reload_cog.error
    async def reload_error(self, ctx, error):
        embed = discord.Embed(title="Fail!",
                              description="You are not allowed to use that command!",
                              color=discord.Color.red())
        await ctx.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTLoader(client))
