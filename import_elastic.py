from elasticsearch import Elasticsearch, helpers
from json_lineage import load
from dotenv import load_dotenv
import os
load_dotenv("elastic-start-local/.env")

ES_LOCAL_API_KEY = os.environ.get("ES_LOCAL_API_KEY")

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9200'], api_key=ES_LOCAL_API_KEY)

# Load data from JSON file
data = load('StackOverflowMini_dbo_Posts.json')

# Prepare data for bulk API
actions = [
    {
        "_index": "post",
        "_source": doc
    }
    for doc in data
]

# Index data in Elasticsearch
helpers.bulk(es, actions)
