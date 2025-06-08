from elasticsearch import AsyncElasticsearch
from es.config.settings import settings

es_client: AsyncElasticsearch | None = None


def init_es_client() -> AsyncElasticsearch:
    return AsyncElasticsearch(
        hosts=settings.es_hosts,
        ca_certs=settings.es_ca_certs,
        basic_auth=settings.es_basic_auth,
        verify_certs=settings.es_verify_certs,
    )


def get_es_client() -> AsyncElasticsearch:
    global es_client
    if es_client is None:
        es_client = init_es_client()
    return es_client


async def close_es_client():
    global es_client
    if es_client:
        await es_client.close()
        es_client = None
