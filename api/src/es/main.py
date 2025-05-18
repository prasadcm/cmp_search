from fastapi import FastAPI
from es.clients.elasticsearch_client import close_es_client
from es.routes import search
from contextlib import asynccontextmanager
from es.config.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    yield
    # Shutdown logic
    await close_es_client()


app = FastAPI(lifespan=lifespan)

setup_logging()

app.include_router(search.router, prefix="/search", tags=["Search"])
