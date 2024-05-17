import logging
from typing import Callable
from fastapi import FastAPI

app = FastAPI()
logger = logging.getLogger(__name__)


def read_from_plex_server() -> str:
    logger.info("Making a read request to the Plex server...")
    return "Read data from Plex server"


def update_plex_server() -> str:
    logger.info("Making an update request to the Plex server...")
    return "Updated data on the Plex server"


@app.get("/read")
async def read_route(response_generator: Callable[[], str] = read_from_plex_server) -> str:
    return response_generator()


@app.post("/update")
async def update_route(response_generator: Callable[[], str] = update_plex_server) -> str:
    return response_generator()


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)
