import os
import json
import discord
from discord.ext import commands


class EXTLogging(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @staticmethod
    @commands.Cog.listener("on_message")
    async def on_message(ctx: discord.Message):
        log: list = []
        if os.path.isfile("cogs/logging/log.json"):
            with open("cogs/logging/log.json", "r", encoding="utf-8") as file:
                log = json.loads(file.read())
        message = {"id": f"{ctx.id}",
                   "guild": f"{ctx.guild.id}",
                   "created_at": f"{ctx.created_at.astimezone()}",
                   "edited_at": f"{ctx.edited_at.astimezone() if ctx.edited_at is not None else None}",
                   "author": f"{ctx.author.id} / {ctx.author.name}",
                   "content": f"{ctx.content}"}
        log.append(message)
        with open("cogs/logging/log.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(log, indent=1))

    @staticmethod
    @commands.Cog.listener("on_message_edit")
    async def on_message_edit(_, ctx: discord.Message):
        log: list = []
        if os.path.isfile("cogs/logging/log.json"):
            with open("cogs/logging/log.json", "r", encoding="utf-8") as file:
                log = json.loads(file.read())
        message = {"id": f"{ctx.id}",
                   "guild": f"{ctx.guild.id}",
                   "created_at": f"{ctx.created_at.astimezone()}",
                   "edited_at": f"{ctx.edited_at.astimezone() if ctx.edited_at is not None else None}",
                   "author": f"{ctx.author.id} / {ctx.author.name}",
                   "content": f"{ctx.content}"}
        log.append(message)
        with open("cogs/logging/log.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(log, indent=1))


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTLogging(client))
