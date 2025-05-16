from fastapi import FastAPI
from es.clients.elasticsearch_client import close_es_client
from es.routes import search
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    yield
    # Shutdown logic
    await close_es_client()


app = FastAPI(lifespan=lifespan)

app.include_router(search.router, prefix="/search", tags=["Search"])
