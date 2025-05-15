from fastapi import FastAPI
from es.routes.search import router as search_router
from es.deps.search import es_client, close_es_client

app = FastAPI()

app.include_router(search_router, prefix="/search", tags=["search"])

@app.on_event("startup")
async def startup():
    await es_client.ping()

@app.on_event("shutdown")
async def shutdown():
    await close_es_client()