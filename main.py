import asyncio

import revolt

from src import Bot


async def main():
    async with revolt.utils.client_session() as session:
        bot = Bot(session)

        await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
