import asyncio

import uvicorn

import fsm

config = uvicorn.Config(
    "app:app",
    port=5000,
    log_level="info",
    access_log=True,
    use_colors=True,
    reload=True,
)
server = uvicorn.Server(config)


async def main() -> None:
    """Run Uvicorn server and FSM concurrently"""
    asyncio.create_task(fsm.run())
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
