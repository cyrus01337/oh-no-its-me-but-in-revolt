import pathlib
import sys
import traceback

import dotenv
import revolt
from revolt.ext import commands


class Bot(commands.CommandsClient):
    def __init__(self, session, *args, **kwargs):
        self.initialised = False
        self.env = dotenv.dotenv_values(".env")
        token = self.env.pop("TOKEN")

        super().__init__(session, token, *args, **kwargs)
        self.load_cogs()

    def load_extension(self, path: str):
        super().load_extension(path)
        self.dispatch("extension_loaded", path)

    def load_cogs(self):
        for file in pathlib.Path("./src/cogs").glob("./**/*.py"):
            extension = f"src.cogs.{file.stem}"

            try:
                self.load_extension(extension)
            except Exception as error:
                self.dispatch("extension_failed", error, extension)

    async def on_extension_loaded(self, extension: str):
        print(f"✔️ Successfully loaded {extension}")

    async def on_extension_failed(self, error: Exception, extension: str):
        print(f"❌ Failed to load {extension}")

        raise error

    async def on_ready(self):
        if self.initialised:
            return

        self.initialised = True

        self.dispatch("startup")

    async def on_startup(self):
        prefix = self.env["PREFIX"]

        print(f'\n{self.user.name} is up with prefix "{prefix}"!', end="\n\n")

    async def get_prefix(self, message: revolt.Message):
        prefix = self.env["PREFIX"]
        is_owner = message.author.id == self.user.owner_id

        if is_owner:
            return [prefix, ""]

        return prefix
