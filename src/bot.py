import dotenv
import revolt
from revolt.ext import commands


class Bot(commands.CommandsClient):
    def __init__(self, session, *args, **kwargs):
        self.initialised = False
        self.env = dotenv.dotenv_values(".env")

        token = self.env.pop("TOKEN")

        super().__init__(session, token, *args, **kwargs)

    async def _startup_hook(self):
        prefix = self.env["PREFIX"]
        print(f'{self.user.name} is up with prefix "{prefix}"!', end="\n\n")

    async def on_ready(self):
        if self.initialised:
            return

        self.initialised = True

        await self._startup_hook()

    async def get_prefix(self, message: revolt.Message):
        prefix = self.env["PREFIX"]
        is_owner = message.author.id == self.user.owner_id

        if is_owner:
            return [prefix, ""]

        return prefix

    async def on_message(self, message: revolt.Message):
        print(message.content)

        await self.process_commands(message)

    @commands.command()
    async def say(self, ctx: commands.Context, *, message: str):
        await ctx.send(message)
