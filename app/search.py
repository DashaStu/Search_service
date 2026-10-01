from elasticsearch import AsyncElasticsearch
import os

ELASTIC_URL = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")
es_client = AsyncElasticsearch(
    [ELASTIC_URL], 
    headers={"Accept": "application/vnd.elasticsearch+json; compatible-with=8",
             "Content-Type": "application/vnd.elasticsearch+json; compatible-with=8"}
)

async def init_index():
    if not await es_client.ping():
        raise Exception("Elasticsearch ping failed!")
    print("Elasticsearch is connected!")