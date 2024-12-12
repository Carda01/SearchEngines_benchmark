import os
#os.chdir("..")  # Change to the parent directory
#print("Current working directory:", os.getcwd())  # Verify the change
from opensearchpy import OpenSearch, helpers
import pandas as pd
from pprint import pp
from dotenv import load_dotenv
from tqdm import tqdm
import os
def ppr(resp):
    pp(resp.raw)


# Connecting to the server
#  
load_dotenv()
# Recupera la variabile della password dall'ambiente
OPENSEARCH_INITIAL_ADMIN_PASSWORD = os.getenv("OPENSEARCH_INITIAL_ADMIN_PASSWORD")
OPENSEARCH_URL = os.getenv("OPENSEARCH_URL")  
# Verifica che la password sia stata caricata correttamente
if OPENSEARCH_INITIAL_ADMIN_PASSWORD:
    print("Password correct.")
else:
    print("Error in the password")


client = OpenSearch(
    hosts=[OPENSEARCH_URL],
    http_auth=("admin", OPENSEARCH_INITIAL_ADMIN_PASSWORD),
    use_ssl=False,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False
)
try:
    info = client.info()
    print("Connection to OpenSearch succesful!")
except Exception as e:
    print(f"Error in the connection: {e}")



### Uploading post data
# 

def generator_post(json_chunk, index_):
    for line in json_chunk:
        yield {
            "_index": index_,
            "_id": line.get('Id'),
            "_source": {
                "Body": line.get("Body",""),
                "CommentCount": line.get("CommentCount",""),
                "CreationDate": line.get("CreationDate",""),
                "OwnerUserId": line.get("OwnerUserId","")
            }
        }
        
def generator_comments(json_chunk, index_):
    for line in json_chunk:
        yield {
            "_index": index_,
            "_id": line.get('Id'),
            "_source": {
                "Text": line.get("Text",""),
                "Score": line.get("Score",""),
                "CreationDate": line.get("CreationDate",""),
                "UserId": line.get("UserId","")
            }
        }


def generator_user(json_chunk, index_):
    for line in json_chunk:
        yield {
            "_index": index_,
            "_id": line.get('Id'),
            "_source": {
                "AboutMe": line.get("AboutMe",""),
                "CreationDate": line.get("CreationDate",""),
                "DisplayName": line.get("DisplayName",""),
                "DownVotes": line.get("DownVotes",""),
                "LastAccessDate": line.get("LastAccessDate",""),
                "UpVotes": line.get("UpVotes","")
            }
        }

def from_chunk_to_client_post(chunk,index_):
    json_chunk = chunk.to_dict("records")
    return generator_post(json_chunk,index_)

def from_chunk_to_client_user(chunk,index_):
    json_chunk = chunk.to_dict("records")
    return generator_user(json_chunk,index_)

def from_chunk_to_client_comments(chunk,index_):
    json_chunk = chunk.to_dict("records")
    return generator_comments(json_chunk,index_)



client.indices.create(
    index='html_posts',
    body = 
    {
    'settings':{
        "analysis": {
            "analyzer": {
                "html_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "char_filter": [
                        "html_strip"
                    ]
                }
            }
        }
    }, 
    'mappings':{
            "properties": {
                "Body": {
                    "type": "text",
                    "analyzer": "html_analyzer"
                },
                "CommentCount": {
                    "type": "integer"
                },
                "CreationDate": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"
                },
                "OwnerUserId": {
                    "type": "integer"
                }
            }
        }
    }
)


columns = ['Id', 'OwnerUserId','Body', 'CommentCount', "CreationDate"]
for chunk in tqdm(pd.read_csv('data/Posts.csv', chunksize=1000)):
    gen = from_chunk_to_client_post(chunk[columns], index_='html_posts')
    res = helpers.bulk(client, gen)

## Reindex post and add custom text analyzer

client.indices.create(
    index="posts_analyzed_v2",
    body={
        "settings": {
            "analysis": {
                "analyzer": {
                    "custom_text_analyzer": {
                        "type": "standard",
                        "stopwords": "_english_"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "Body": {
                    "type": "text",
                    "analyzer": "custom_text_analyzer",
                    "fielddata": True
                },
                "CommentCount": {"type": "long"},
                "CreationDate": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"  # Example formats
                },
                "OwnerUserId": {"type": "long"}
            }
        }
    }
)

client.reindex(
    body={
        "source": {"index": "html_posts"},
        "dest": {"index": "posts_analyzed_v2"}
    },
    request_timeout=1000  # Increase timeout if needed
)


# Fetch and print all indices
indices = client.cat.indices(format="json")  # Fetch in JSON format for easier processing
for index in indices:
    print(f"Index: {index['index']}, Health: {index['health']}, Docs Count: {index['docs.count']}, Size: {index['store.size']}")


## Uploading comments

client.indices.create(
    index="comments",
    body={
        "settings": {
            "analysis": {
                "analyzer": {
                    "custom_text_analyzer": {
                        "type": "standard",
                        "stopwords": "_english_"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "Text": {
                    "type": "text",
                    "analyzer": "custom_text_analyzer",
                    "fielddata": True
                },
                "Score": {"type": "long"},
                "CreationDate": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"  # Example formats
                },
                "UserId": {"type": "long"},
                "Id": {"type": "long"}
            }
        }
    }
)


columns = ['Id', 'UserId','Text', 'Score', "CreationDate"]
for chunk in tqdm(pd.read_csv('data/Comments.csv', chunksize=1000)):
    # Replace NaN values in the 'UserId' column with a default value, e.g., -1
    chunk['UserId'] = chunk['UserId'].fillna(-1).astype(int)  # Replace with a default value like -1
    # Ensure all columns conform to expected data types
    chunk['Score'] = chunk['Score'].fillna(0).astype(int)
    gen = from_chunk_to_client_comments(chunk[columns], index_='comments')
    res = helpers.bulk(client, gen)

## Uploading the user data


client.indices.create(
    index="users",
    body={
        "settings": {
            "analysis": {
                "analyzer": {
                    "custom_text_analyzer": {
                        "type": "standard",
                        "stopwords": "_english_"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "AboutMe": {
                    "type": "text",
                    "analyzer": "custom_text_analyzer",
                    "fielddata": True
                },
                "Score": {"type": "long"},
                "CreationDate": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"  # Example formats
                },
                "LastAccessDate": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"  # Example formats
                },
                "UserId": {"type": "long"},
                "Id": {"type": "long"},
                "UpVotes": {"type": "long"},
                "DownVotes": {"type": "long"},
                "DisplayName":{"type": "text"}
            }
        }
    }
)

columns = ['Id', 'AboutMe', 'CreationDate','DisplayName', 'DownVotes','LastAccessDate','UpVotes']
for chunk in tqdm(pd.read_csv('data/Users.csv', chunksize=1000)):
    chunk['AboutMe'] = chunk['AboutMe'].fillna(" ")
    chunk['DisplayName'] = chunk['DisplayName'].fillna(" ")
    gen = from_chunk_to_client_user(chunk[columns], index_='users')
    res = helpers.bulk(client, gen)

