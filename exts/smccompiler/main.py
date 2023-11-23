import io
import discord
from discord.ext import commands
from exts.smccompiler.compiler import precompile, split_bytecode, bytecode
from exts.smccompiler.emulator import emulate_mq8b


class EXTCompiler(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="smc", description="compiles the code for MQA")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def smc(self, ctx: commands.context.Context, *, code: str | None = None):
        # if the argument was given (aka the code is inside the message)
        if code:
            # remove the '```'
            code = code.lstrip("`").rstrip("`")

        # if the code was inside the attachment
        else:
            # check if there are any attachments
            if len(ctx.message.attachments) > 0:
                # .replace("\r\n", "\n") cuz sometimes that's a thing
                code = (await ctx.message.attachments[0].read()).decode("utf-8").replace("\r\n", "\n")

            # if there are no attachments, raise an error
            else:
                raise commands.MissingRequiredArgument(commands.Parameter("code", commands.Parameter.POSITIONAL_ONLY))

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
            bc += f"{idx:0>4} | {line[0]: ^3} | {bin(line[2])[2:]:0>8} | {bin(line[1])[2:]:0>7}\n"

        # write to the compiler output
        compiler_output += bc

        # send message
        await ctx.send(file=discord.File(fp=io.BytesIO(compiler_output.encode("ascii")),
                                         filename="compiler_output.txt"),
                       reference=ctx.message)

    @smc.error
    async def smc_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Be patient!",
                                  description=f"Please wait: {error.retry_after:.2f} seconds",
                                  color=discord.Color.orange())
            await ctx.send(embed=embed, reference=ctx.message)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="No code was given",
                                  description="You forgot to provide the source code",
                                  color=discord.Color.orange())
            await ctx.send(embed=embed, reference=ctx.message)
        else:
            embed = discord.Embed(title="ded...",
                                  description=f"idk what happened, it ded. {type(error)}",
                                  color=discord.Color.orange())
            await ctx.send(embed=embed, reference=ctx.message)

    @commands.command(name="sme", description="emulates the code for MQA")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sme(self, ctx: commands.context.Context, *, code: str | None = None):
        # if the argument was given (aka the code is inside the message)
        if code:
            # remove the '```'
            code = code.lstrip("`").rstrip("`")

        # if the code was inside the attachment
        else:
            # check if there are any attachments
            if len(ctx.message.attachments) > 0:
                # .replace("\r\n", "\n") cuz sometimes that's a thing
                code = (await ctx.message.attachments[0].read()).decode("utf-8").replace("\r\n", "\n")

            # if there are no attachments, raise an error
            else:
                raise commands.MissingRequiredArgument(commands.Parameter("code", commands.Parameter.POSITIONAL_ONLY))

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

    @sme.error
    async def sme_handler(self, ctx, error):
        # it's basically the same thing
        await self.smc_handler(ctx, error)

    @commands.command(name="smcb", description="compiles the code for MQA and returns bytecode")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def smcb(self, ctx: commands.context.Context, *, code: str | None = None):
        # if the argument was given (aka the code is inside the message)
        if code:
            # remove the '```'
            code = code.lstrip("`").rstrip("`")

        # if the code was inside the attachment
        else:
            # check if there are any attachments
            if len(ctx.message.attachments) > 0:
                # .replace("\r\n", "\n") cuz sometimes that's a thing
                code = (await ctx.message.attachments[0].read()).decode("utf-8").replace("\r\n", "\n")

            # if there are no attachments, raise an error
            else:
                raise commands.MissingRequiredArgument(commands.Parameter("code", commands.Parameter.POSITIONAL_ONLY))

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

        binary = bytes()
        for data in bytecode(decoded):
            binary += bytes([data >> 8, data & 0xff])

        # send message
        await ctx.send(file=discord.File(fp=io.BytesIO(binary),
                                         filename="compiler_output.bin"),
                       reference=ctx.message)

    @smcb.error
    async def smcb_handler(self, ctx, error):
        # it's basically the same thing
        await self.smc_handler(ctx, error)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTCompiler(client))
