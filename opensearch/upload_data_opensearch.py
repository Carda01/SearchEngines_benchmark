import os
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
OPENSEARCH_INITIAL_ADMIN_PASSWORD = os.getenv("OPENSEARCH_INITIAL_ADMIN_PASSWORD")
OPENSEARCH_URL = os.getenv("OPENSEARCH_URL")  
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



def generator_post(json_chunk, index_):
    for line in json_chunk:
        yield {
            "_index": index_,
            "_id": line.get('Id'),
            "_source": {
                "Body": line.get("Body",""),
                "CommentCount": line.get("CommentCount",""),
                "CreationDate": line.get("CreationDate",""),
                "OwnerUserId": line.get("OwnerUserId",""),
                "ClosedDate": line.get("ClosedDate",""),
                "Title": line.get("Title",""),
                "Tags": line.get("Tags",""),
                "FavoriteCount": line.get("FavoriteCount",""),
                "Score": line.get("Score","")
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
                "UpVotes": line.get("UpVotes",""),
                "Reputation": line.get("Reputation",""),
                "Location": line.get("Location","")
            }
        }
        


def generator_commentsjoinuser(json_chunk, index_):
    for line in json_chunk:
        yield {
            "_index": index_,
            "_id": line.get('Id'),
            "_source": {
                "Text": line.get("Text",""),
                "Score": line.get("Score",""),
                "CreationDate": line.get("CreationDate",""),
                "UserId": line.get("UserId",""),
                "AboutMe": line.get("AboutMe",""),
                "CreationDateUser": line.get("CreationDateUser",""),
                "DisplayName": line.get("DisplayName",""),
                "DownVotes": line.get("DownVotes",""),
                "LastAccessDate": line.get("LastAccessDate",""),
                "UpVotes": line.get("UpVotes",""),
                "Reputation": line.get("Reputation",""),
                "Location": line.get("Location",""),
                "Age": line.get("Age","")
            }
        }

def generator_postsjoinuser(json_chunk, index_):
    for line in json_chunk:
        yield {
            "_index": index_,
            "_id": line.get('Id'),
            "_source": {
                "Body": line.get("Body",""),
                "CommentCount": line.get("CommentCount",""),
                "CreationDate": line.get("CreationDate",""),
                "OwnerUserId": line.get("OwnerUserId",""),
                "ClosedDate": line.get("ClosedDate",""),
                "Title": line.get("Title",""),
                "Tags": line.get("Tags",""),
                "FavoriteCount": line.get("FavoriteCount",""),
                "Score": line.get("Score",""),    
                "UserId": line.get("UserId",""),
                "AboutMe": line.get("AboutMe",""),
                "CreationDateUser": line.get("CreationDateUser",""),
                "DisplayName": line.get("DisplayName",""),
                "DownVotes": line.get("DownVotes",""),
                "LastAccessDate": line.get("LastAccessDate",""),
                "UpVotes": line.get("UpVotes",""),
                "Reputation": line.get("Reputation",""),
                "Location": line.get("Location",""),
                "Age": line.get("Age","")
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

def from_chunk_to_client_commentsjoinuser(chunk,index_):
    json_chunk = chunk.to_dict("records")
    return generator_commentsjoinuser(json_chunk,index_)

def from_chunk_to_client_postsjoinuser(chunk,index_):
    json_chunk = chunk.to_dict("records")
    return generator_postsjoinuser(json_chunk,index_)


client.indices.create(
    index="posts",
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
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"  
                },
                "OwnerUserId": {"type": "long"},
                "ClosedDate": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"  
                },
                "Title": {
                    "type": "text",
                     "analyzer": "custom_text_analyzer",
                    "fielddata": True
                },
                "Tags": {
                        "type": "text",
                        "analyzer": "custom_text_analyzer",
                        "fielddata": True
                },
                "FavoriteCount": {"type": "long"},
                "Score": {"type": "long"}
            }
        }
    }
)


columns = ['Id', 'Body', 'CommentCount', 'CreationDate', 'OwnerUserId', 'ClosedDate', 'Title', 'Tags','FavoriteCount', 'Score']
for chunk in tqdm(pd.read_csv('data/Posts.csv', chunksize=1000)):
    chunk['ClosedDate'] = chunk['ClosedDate'].fillna("2070-01-01 00:00:00.000")
    chunk['Title'] = chunk['Title'].fillna("Nan")
    chunk['Tags'] = chunk['Tags'].fillna("Nan")
    gen = from_chunk_to_client_post(chunk[columns], index_='posts')
    res = helpers.bulk(client, gen)


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
                "DisplayName":{"type": "text"},
                "Location":{"type": "text"},
                "Reputation":{"type": "long"}
            }
        }
    }
)


columns = ['Id', 'AboutMe', 'CreationDate','DisplayName', 'DownVotes','LastAccessDate','UpVotes','Reputation', 'Location']
for chunk in tqdm(pd.read_csv('data/Users.csv', chunksize=1000)):
    chunk['AboutMe'] = chunk['AboutMe'].fillna("Nan")
    chunk['DisplayName'] = chunk['DisplayName'].fillna("Nan")
    chunk['Location'] = chunk['Location'].fillna("Nan")
    gen = from_chunk_to_client_user(chunk[columns], index_='users')
    res = helpers.bulk(client, gen)

print('creating Join index')

# Load Users and Comments data
users = pd.read_csv("data/Users.csv")[['Id', 'AboutMe', 'CreationDate','DisplayName', 'DownVotes','LastAccessDate','UpVotes','Reputation', 'Location','Age']]
comments = pd.read_csv("data/Comments.csv")

# Merge comments with user data on UserId
comments_join_users = comments.merge(users, left_on="UserId", right_on="Id", how="left")

comments_join_users.drop(columns=['Id_y'], inplace=True)
comments_join_users.rename(columns={'Id_x':'Id', 'CreationDate_y':'CreationDateUser', 'CreationDate_x':'CreationDate'}, inplace=True)


cols_commentsjoinuser=['Id', 'CreationDate', 'Score', 'Text', 'UserId',
                        'AboutMe', 'CreationDateUser', 'DisplayName', 'DownVotes',
                        'LastAccessDate', 'UpVotes', 'Reputation', 'Location', 'Age']


comments_join_users = comments_join_users[cols_commentsjoinuser]

comments_join_users['AboutMe'] = comments_join_users['AboutMe'].fillna("Nan")
comments_join_users['DisplayName'] = comments_join_users['DisplayName'].fillna("Nan")
comments_join_users['Location'] = comments_join_users['Location'].fillna("Nan")
comments_join_users['Age'] = comments_join_users['Age'].fillna(0).astype(int)
comments_join_users['UserId'] = comments_join_users['UserId'].fillna(-1).astype(int)  # Replace with a default value like -1
comments_join_users['Score'] = comments_join_users['Score'].fillna(0).astype(int)
comments_join_users['CreationDateUser'] = comments_join_users['CreationDateUser'].fillna("2070-01-01 00:00:00.000")
comments_join_users['LastAccessDate'] = comments_join_users['LastAccessDate'].fillna("2070-01-01 00:00:00.000")

comments_join_users['Reputation'] = comments_join_users['Reputation'].fillna(0).astype(int)
comments_join_users['UpVotes'] = comments_join_users['UpVotes'].fillna(0).astype(int)
comments_join_users['DownVotes'] = comments_join_users['DownVotes'].fillna(0).astype(int)

comments_join_users.to_csv('data/commentsjoinuser.csv')


client.indices.create(
    index="commentsjoinusers",
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
                "Id": {"type": "long"},
                "AboutMe": {
                    "type": "text",
                    "analyzer": "custom_text_analyzer",
                    "fielddata": True
                },
                "Score": {"type": "long"},
                "CreationDateUser": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"  
                },
                "LastAccessDate": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"  
                },
                "UserId": {"type": "long"},
                "UpVotes": {"type": "long"},
                "DownVotes": {"type": "long"},
                "DisplayName":{"type": "text"},
                "Location":{"type": "text"},
                "Reputation":{"type": "long"},
                "Age":{"type": "long"}
            }
        }
    }
)

for chunk in tqdm(pd.read_csv('data/commentsjoinuser.csv', chunksize=1000)):
    gen = from_chunk_to_client_commentsjoinuser(chunk, index_='commentsjoinusers')
    res = helpers.bulk(client, gen)


post = pd.read_csv('data/Posts.csv')
post = post[['Id', 'Body', 'CommentCount', 'CreationDate', 'OwnerUserId', 'ClosedDate', 'Title', 'Tags','FavoriteCount', 'Score']]

# Merge comments with user data on UserId
posts_join_users = post.merge(users, left_on="OwnerUserId", right_on="Id", how="left")

posts_join_users.drop(columns=['Id_y'], inplace=True)
posts_join_users.rename(columns={'Id_x':'Id', 'CreationDate_y':'CreationDateUser', 'CreationDate_x':'CreationDate'}, inplace=True)

cols_postsjoinuser = ['Id', 'Body', 'CommentCount', 'CreationDate', 'OwnerUserId', 'ClosedDate', 'Title', 'Tags','FavoriteCount', 'Score', 
                     'AboutMe', 'CreationDateUser','DisplayName', 'DownVotes','LastAccessDate','UpVotes','Reputation', 'Location','Age']


posts_join_users = posts_join_users[cols_postsjoinuser]

posts_join_users['AboutMe'] = posts_join_users['AboutMe'].fillna("Nan")
posts_join_users['DisplayName'] = posts_join_users['DisplayName'].fillna("Nan")
posts_join_users['Location'] = posts_join_users['Location'].fillna("Nan")
posts_join_users['Age'] = posts_join_users['Age'].fillna(0).astype(int)
# posts_join_users['UserId'] = posts_join_users['UserId'].fillna(-1).astype(int)  # Replace with a default value like -1
posts_join_users['Score'] = posts_join_users['Score'].fillna(0).astype(int)
posts_join_users['CreationDateUser'] = posts_join_users['CreationDateUser'].fillna("2070-01-01 00:00:00.000")
posts_join_users['LastAccessDate'] = posts_join_users['LastAccessDate'].fillna("2070-01-01 00:00:00.000")

posts_join_users['Reputation'] = posts_join_users['Reputation'].fillna(0).astype(int)
posts_join_users['UpVotes'] = posts_join_users['UpVotes'].fillna(0).astype(int)
posts_join_users['DownVotes'] = posts_join_users['DownVotes'].fillna(0).astype(int)

posts_join_users['ClosedDate'] = posts_join_users['ClosedDate'].fillna("2070-01-01 00:00:00.000")
posts_join_users['Title'] = posts_join_users['Title'].fillna("Nan")
posts_join_users['Tags'] = posts_join_users['Tags'].fillna("Nan")

posts_join_users.to_csv('data/postjoinuser.csv')

client.indices.create(
    index="postsjoinusers",
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
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"  
                },
                "OwnerUserId": {"type": "long"},
                "ClosedDate": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"  
                },
                "Title": {
                    "type": "text",
                     "analyzer": "custom_text_analyzer",
                    "fielddata": True
                },
                "Tags": {
                        "type": "text",
                        "analyzer": "custom_text_analyzer",
                        "fielddata": True
                },
                "FavoriteCount": {"type": "long"},

                "Score": {"type": "long"},
                "Id": {"type": "long"},
                "AboutMe": {
                    "type": "text",
                    "analyzer": "custom_text_analyzer",
                    "fielddata": True
                },
                "CreationDateUser": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"  
                },
                "LastAccessDate": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"  
                },
                "UserId": {"type": "long"},
                "UpVotes": {"type": "long"},
                "DownVotes": {"type": "long"},
                "DisplayName":{"type": "text"},
                "Location":{"type": "text"},
                "Reputation":{"type": "long"},
                "Age":{"type": "long"}
            }
        }
    }
)

for chunk in tqdm(pd.read_csv('data/postjoinuser.csv', chunksize=1000)):
    gen = from_chunk_to_client_postsjoinuser(chunk, index_='postsjoinusers')
    res = helpers.bulk(client, gen)


