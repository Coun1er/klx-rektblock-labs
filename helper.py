import asyncio


def retry(func):
    attempts = 5
    delay = 5

    async def wrapper(*args, **kwargs):
        for _ in range(attempts):
            result = await func(*args, **kwargs)

            if result:
                return True

            await asyncio.sleep(delay)

        return False

    return wrapper
