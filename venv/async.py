import asyncio
import random


async def two(x):
    await asyncio.sleep(random.randint(1, 6))
    print(x)


async def one(x):
    await asyncio.sleep(random.randint(1, 6))
    print(x)


async def main():
    task1 = asyncio.create_task(one(1))
    task2 = asyncio.create_task(two(2))
    await task1
    await task2

asyncio.run(main())