import discord
from discord.ext import commands
from discord import app_commands
from exts.smccompiler.compiler import precompile_code, to_bytecode


class EXTCompiler(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="smcc8")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def smcc8(self, ctx: commands.context.Context, *, code: str):
        # remove the '```'
        code = code.lstrip("`").rstrip("`")

        # try to compile the code
        try:
            decoded = precompile_code(code)

        # send error if fail
        except Exception as e:
            embed = discord.Embed(title="Precompiler error!",
                                  description=str(e),
                                  color=discord.Color.red())
            await ctx.send(embed=embed, reference=ctx.message)
            return

        # precompiled code message
        precompiled = "```\n"
        for idx, line in enumerate(decoded):
            # check if flag bit is on
            # if it is not, add nothing
            if line['flag'] == 0:
                precompiled += f"{idx:0>4} | {line['comp'][0]: <5} {line['comp'][1]: <4}"

            # if it is, add '*'
            else:
                precompiled += f"{idx:0>4} | {line['comp'][0]: <5} *{line['comp'][1]: <4}"

            # if it's not last line add '\n', else add a cap
            if idx + 1 != len(decoded):
                precompiled += "\n"
            else:
                precompiled += "\n```"

        # send precompiled version
        await ctx.send(precompiled, reference=ctx.message)

        # process the bytecode version
        decoded = to_bytecode(decoded)

        bytecode = "```"
        for idx, line in enumerate(decoded):
            bytecode += f"{idx:0>4} | {line[0]: ^3} | {bin(line[1])[2:]:0>7} | {bin(line[2])[2:]:0>8}"

            # if it's not last line add '\n', else add a cap
            if idx + 1 != len(decoded):
                bytecode += "\n"
            else:
                bytecode += "\n```"

        # send bytecode version
        await ctx.send(bytecode, reference=ctx.message)

    @smcc8.error
    async def smcc8_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Be patient!",
                                  description=f"Please wait: {error.retry_after:.2f} seconds",
                                  color=discord.Color.orange())
            await ctx.send(embed=embed, reference=ctx.message)
        elif isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(title="Output is too long :(",
                                  description="Unable to print the full message.",
                                  color=discord.Color.orange())
            await ctx.send(embed=embed, reference=ctx.message)
        else:
            embed = discord.Embed(title="ded...",
                                  description=f"idk what happened, it ded. {type(error)}",
                                  color=discord.Color.orange())
            await ctx.send(embed=embed, reference=ctx.message)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTCompiler(client))
