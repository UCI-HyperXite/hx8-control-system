import asyncio


async def run_periodic() -> None:
    while True:
        print("tick")
        await asyncio.sleep(1)
