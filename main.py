import asyncio

from kiloex import Kiloex
from logs import color_ml, head_text, logger

with open("pk.txt", "r") as f:
    private_keys = f.read().splitlines()


async def run_wallet(private_key: str):
    client = Kiloex(private_key=private_key)

    await client.run()


async def main():
    logger.info(color_ml(head_text))
    await asyncio.gather(*[run_wallet(k) for k in private_keys])


if __name__ == "__main__":
    asyncio.run(main())
