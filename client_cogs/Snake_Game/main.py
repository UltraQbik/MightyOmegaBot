import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from client_cogs.Snake_Game.snake import Snake, CollisionException
from client_cogs.Snake_Game.player import Direction


class EXTSnake(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.sessions = {}

    @app_commands.command(
        name="snake",
        description="play snake")
    @app_commands.describe(
        size="Size of field. Can be number from 2 to 14 (default: 9)")
    async def snake(
        self,
        interaction: discord.Interaction,
        size: int = 9
    ) -> None:
        if size < 2 or size > 14:
            await interaction.response.send_message(
                "Size should be number from 1 to 14",
                ephemeral=True
            )
        snake: Snake = Snake(field_size=size)
        await interaction.response.send_message(f"Snake:\n{snake}")
        message = await interaction.original_response()
        for emoji in "⬅️", "⬇️", "⬆️", "➡️":
            await message.add_reaction(emoji)
        self.sessions[message.id] = snake
        try:
            while True:
                snake.do_tick()
                message = await message.edit(
                    content=f"Snake:\n{snake}\nScore: {snake.score}"
                )
                await asyncio.sleep(3)
        except CollisionException:
            await message.edit(content=f"{message.content}\nGame over!")
        self.sessions.pop(message.id)

    @commands.Cog.listener()
    @commands.has_permissions(manage_messages=True)
    async def on_raw_reaction_add(
        self,
        payload: discord.RawReactionActionEvent
    ) -> None:
        if payload.message_id not in self.sessions or \
           payload.emoji.name not in "⬅️⬆️⬇️➡️" or \
           not payload.member:
            return
        channel = await self.client.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.remove_reaction(payload.emoji, payload.member)
        if payload.message_id not in self.sessions:
            return
        snake = self.sessions[payload.message_id]
        match payload.emoji.name:
            case "⬅️":
                if snake.direction != Direction.RIGHT:
                    snake.direction = Direction.LEFT
            case "⬆️":
                if snake.direction != Direction.DOWN:
                    snake.direction = Direction.UP
            case "⬇️":
                if snake.direction != Direction.UP:
                    snake.direction = Direction.DOWN
            case "➡️":
                if snake.direction != Direction.LEFT:
                    snake.direction = Direction.RIGHT


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTSnake(client))
