import asyncio


async def run_periodic() -> None:
    while True:
        try:
            print("tick")
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            # currently not working :(
            break
