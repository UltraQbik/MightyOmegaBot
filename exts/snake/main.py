import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from exts.snake.snake import Snake, CollisionException
from exts.snake.player import Direction


class EXTSnake(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.sessions = {}

    @app_commands.command(
        name="snake",
        description="play snake")
    async def snake(
        self,
        interaction: discord.Interaction,
    ) -> None:
        snake: Snake = Snake()
        await interaction.response.send_message(f"Snake:\n{snake}")
        message = await interaction.original_response()
        for emoji in "⬅️", "⬇️", "⬆️", "➡️":
            await message.add_reaction(emoji)
        self.sessions[message.id] = snake
        try:
            while True:
                snake.do_tick()
                message = await message.edit(content=f"Snake:\n{snake}")
                await asyncio.sleep(1)
        except CollisionException:
            await message.edit(content=f"{message.content}\nGame over!")
        self.sessions.pop(message.id)

    @commands.Cog.listener()
    @commands.has_permissions(manage_messages=True)
    async def on_raw_reaction_add(
        self,
        payload: discord.RawReactionActionEvent
    ) -> None:
        if payload.message_id not in self.sessions or payload.emoji.name not in "⬅️⬆️⬇️➡️" or not payload.member:
            return
        channel = await self.client.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.remove_reaction(payload.emoji, payload.member)
        snake = self.sessions[payload.message_id]
        match payload.emoji.name:
            case "⬅️":
                snake.direction = Direction.LEFT
            case "⬆️":
                snake.direction = Direction.UP
            case "⬇️":
                snake.direction = Direction.DOWN
            case "➡️":
                snake.direction = Direction.RIGHT


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTSnake(client))

