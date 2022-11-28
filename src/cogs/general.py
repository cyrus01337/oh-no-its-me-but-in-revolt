from revolt.ext import commands


class General(commands.Cog):
    @commands.command()
    async def say(self, ctx: commands.Context, *, text: str):
        await ctx.send(text)


def setup(bot):
    bot.add_cog(General())
