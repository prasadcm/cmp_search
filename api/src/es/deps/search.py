from elasticsearch import AsyncElasticsearch

# Initialize client
es_client = AsyncElasticsearch(
    hosts=["https://localhost:9200"],
    ca_certs="../shared/certs/ca/ca.crt",
    basic_auth=("elastic", "elasticpassword"),
    verify_certs=False,
)


# Dependency injection
async def get_es():
    return es_client


# Graceful shutdown
async def close_es_client():
    await es_client.close()
