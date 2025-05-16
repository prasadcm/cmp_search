from es.clients.elasticsearch_client import get_es_client


async def get_es():
    return get_es_client()
