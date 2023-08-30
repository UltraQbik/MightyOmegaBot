import io
import discord
from discord.ext import commands
from exts.smccompiler.compiler import precompile, split_bytecode, bytecode
from exts.smccompiler.emulator import emulate_mq8b


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
            decoded = precompile(code)

        # send error if fail
        except Exception as e:
            embed = discord.Embed(title="Compiler error!",
                                  description=str(e),
                                  color=discord.Color.red())
            await ctx.send(embed=embed, reference=ctx.message)
            return

        # BytesIO
        compiler_output = ""

        # precompiled code message
        precompiled = f"{'- Compiled version -':=^32}\n"
        for idx, line in enumerate(decoded):
            # check if flag bit is on
            # if it is not, add nothing
            if line['flag'] == 0:
                precompiled += f"{idx:0>4} | {line['comp'][0]: <5} {line['comp'][1]: <4}\n"

            # if it is, add '*'
            else:
                precompiled += f"{idx:0>4} | {line['comp'][0]: <5} *{line['comp'][1]: <4}\n"

        # write to the compiler output
        compiler_output += precompiled

        # process the bytecode version
        decoded = split_bytecode(decoded)

        bc = f"\n{'- Bytecode version -':=^32}\n"
        for idx, line in enumerate(decoded):
            bc += f"{idx:0>4} | {line[0]: ^3} | {bin(line[1])[2:]:0>7} | {bin(line[2])[2:]:0>8}\n"

        # write to the compiler output
        compiler_output += bc

        # send message
        await ctx.send(file=discord.File(fp=io.BytesIO(compiler_output.encode("ascii")),
                                         filename="compiler_output.txt"),
                       reference=ctx.message)

    @smcc8.error
    async def smcc8_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Be patient!",
                                  description=f"Please wait: {error.retry_after:.2f} seconds",
                                  color=discord.Color.orange())
            await ctx.send(embed=embed, reference=ctx.message)
        else:
            embed = discord.Embed(title="ded...",
                                  description=f"idk what happened, it ded. {type(error)}",
                                  color=discord.Color.orange())
            await ctx.send(embed=embed, reference=ctx.message)

    @commands.command(name="smce8")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def smce8(self, ctx: commands.context.Context, *, code: str):
        # remove the '```'
        code = code.lstrip("`").rstrip("`")

        # try to compile the code
        try:
            bc = bytecode(precompile(code))

        # send error if fail
        except Exception as e:
            embed = discord.Embed(title="Compiler error!",
                                  description=str(e),
                                  color=discord.Color.red())
            await ctx.send(embed=embed, reference=ctx.message)
            return

        await ctx.send(file=discord.File(fp=io.BytesIO(emulate_mq8b(bc)),
                                         filename="terminal_output.txt"),
                       reference=ctx.message)

    @smce8.error
    async def smcc8_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Be patient!",
                                  description=f"Please wait: {error.retry_after:.2f} seconds",
                                  color=discord.Color.orange())
            await ctx.send(embed=embed, reference=ctx.message)
        else:
            embed = discord.Embed(title="ded...",
                                  description=f"idk what happened, it ded. {type(error)}",
                                  color=discord.Color.orange())
            await ctx.send(embed=embed, reference=ctx.message)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTCompiler(client))
