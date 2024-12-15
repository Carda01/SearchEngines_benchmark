from opensearchpy import OpenSearch, helpers

#Query 1
#Search for comments that contain the word 'Python' and order them by their score.
def query1_os(client):
    resp = client.search(
    index="comments",  # Replace with your actual index name
    body={
            "size": 20,  # Top 20 results
            "query": {
                "match": {
                    "Text": "python"  # text containing 'python'
                }
            },
            "_source": ["id", "Score"],  # Select only id and Score fields
            "sort": [
                {"Score": {"order": "desc"}}  # Sort by Score in descending order
            ]
        }
    )
    return resp

#Query 2
#Search for posts that contain the word 'Python' in the title, that have been closed and ordered by score 
def query2_os(client):
    resp = client.search(
    index="posts",  # Replace with your actual index name
    body={
        "size": 20,  # Top 20 results
        "query": {
            "bool": {
                "must": [
                    {"match": {"Title": "python"}}  # title containing 'python'
                ],
                "filter": [
                    {"exists": {"field": "ClosedDate"}},  # Ensure ClosedDate exists
                    {"range": {
                        "ClosedDate": {
                            "lt": '2070-01-01 00:00:00.000'  # ClosedDate should not be 0
                        }
                    }}
                ]
            }
        },
        "_source": ["id", "Score"],  # Select only id and Score fields
        "sort": [
            {"Score": {"order": "desc"}}  # Sort by Score in descending order
        ]
    }
)
    return resp


#Query 3
#Search for users that contain the word 'Python' AND 'SQL' AND 'Java' in the AboutMe and order by their reputation and last access date
def query3_os(client):
    resp = client.search(
    index="users",  # Replace with your actual index name
    body={
        "size": 20,  # Top 20 results
        "query": {
            "bool": {
                "must": [
                    {"match": {"AboutMe": "python"}},  # AboutMe containing 'python'
                    {"match": {"AboutMe": "sql"}}     # AboutMe containing 'sql'
                ],
                "should": [
                    {"match": {"AboutMe": "java"}},    # AboutMe containing 'java'
                    {"match": {"AboutMe": "javascript"}}  # AboutMe containing 'javascript'
                ],
                "minimum_should_match": 1  # At least one of the should conditions must match
            }
        },
        "_source": ["AccountId", "Reputation", "LastAccessDate"],  # Select only the required fields
        "sort": [
            {"Reputation": {"order": "desc"}},  # Sort by Reputation in descending order
            {"LastAccessDate": {"order": "desc"}}  # Sort by LastAccessDate in descending order
        ]
    }
    )
    return resp


#Query 4
#Search for posts that contain the word 'Python' OR 'SQL' and that have more than 3 Favoirite counts
def query4_os(client):
    resp = client.search(
    index="posts",  # Replace with your actual index name
    body={
        "size": 20,  # Top 20 results
        "query": {
            "bool": {
                "must": [
                    {"range": {"FavoriteCount": {"gt": 3}}}  # Filter for FavoriteCount > 3
                ],
                "should": [
                    {"match": {"Body": "python"}},  # Body containing 'python'
                    {"match": {"Body": "sql"}}  # Body containing 'sql'
                ],
                "minimum_should_match": 1  # At least one of the should conditions must match
            }
        },
        "_source": ["id"]  # Select only the 'id' field
    }
    )
    return resp

#Query 5
#Search for comments that contain the word 'Python' BUT NOT 'SQL' created in 2008
def query5_os(client):
    resp = client.search(
    index="comments",  # Replace with your actual index name
    body={
        "size": 20,  # Top 20 results
        "query": {
            "bool": {
                "must": [
                    {"match": {"Text": "python"}},  # Text containing 'python'
                ],
                "must_not": [
                    {"match": {"Text": "sql"}},  # Text not containing 'sql'
                ],
                "filter": [
                    {"range": {
                        "CreationDate": {
                            "gte": "2008-01-01 00:00:00.000",  # Start of 2008 with time
                            "lt": "2009-01-01 00:00:00.000"  # Start of 2009 with time
                        }
                    }}
                ]
            }
        },
        "_source": ["id", "CreationDate"]  # Select only id and CreationDate fields
    }
    )
    return resp

#Query 6
#Search for the users without downvotes that contain the word 'Python' OR 'SQL' in their AboutMe but double the value on the ranking of the word 'SQL'
def query6_os(client):
    resp = client.search(
    index="users",  # Replace with your actual index name
    body={
        "query": {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {"match": {"AboutMe": "Python"}},  # Match 'Python' in 'AboutMe'
                                {"match": {"AboutMe": "SQL"}}     # Match 'SQL' in 'AboutMe'
                            ],
                            "minimum_should_match": 1  # Equivalent to 'OR' in Sphinx
                        }
                    }
                ],
                "filter": [
                    {"term": {"DownVotes": 0}}  # Filter for DownVotes=0
                ]
            }
        },
        "_source": ["id", "DownVotes"],  # Retrieve 'id' and 'DownVotes' fields
        "sort": [
            {"DownVotes": {"order": "desc"}}  # Sort by DownVotes in descending order
        ]
    }
    )
    return resp

#Query 7
#Search for posts that their body start with the <p>, their title ends with sql and they contain the word sql in their tags
def query7_os(client):
    resp = client.search(
    index="posts",
    body={
        "size": 20,  # Fetch the top 20 results
        "query": {
            "bool": {
                "must": [
                    {"match": {"Body": "<p>"}},
                    {"match": {"Title": "sql"}},
                    {"match": {"Tags":"sql"}}
                ]
            }
        },
        # Return specific fields
        "_source": ["Body", "Title", "Tags", "Score"]
    }
    )
    return resp


#Query 8
#Search for users  who have in their about me Python and SQL but if they have any additional programming lenguage rank them higher, and display the weight of the ranking.
def query8_os(client):
    resp = client.search(
    index="users",  # Replace with your actual index name
    body={
        "query": {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {"match": {"AboutMe": "python"}},  # Match 'python' in 'aboutme'
                                {"match": {"AboutMe": "sql"}},    # Match 'sql' in 'aboutme'
                                {
                                    "bool": {
                                        "should": [
                                            {"match": {"AboutMe": "c++"}},  # Match 'c++' in 'aboutme'
                                            {"match": {"AboutMe": "r"}},    # Match 'r' in 'aboutme'
                                            {"match": {"AboutMe": "ruby"}}, # Match 'ruby' in 'aboutme'
                                            {"match": {"AboutMe": "php"}},  # Match 'php' in 'aboutme'
                                            {"match": {"AboutMe": "java"}}, # Match 'java' in 'aboutme'
                                            {"match": {"AboutMe": "javascript"}} # Match 'javascript' in 'aboutme'
                                        ]
                                    }
                                }
                            ],
                            "minimum_should_match": 1  # At least one condition should match
                        }
                    }
                ]
            }
        },
        "_source": ["id"],  # Retrieve only 'id'
    }
    )
    return resp

#Query 9 
#Search for posts with python in the title, sql in the body and c++ in the tags and order them by score. 
def query9_os(client):
    resp = client.search(
    index="posts",
    body={
        "size": 20,  # Retrieve the top 20 results
        "query": {
            "bool": {
                "must": [  # Match all conditions
                    {"match": {"Body": "sql"}},  # Body contains "sql"
                    {"match": {"Body": "python"}},  # Body contains "python"
                    {"match": {"Body": "c++"}}  # Body contains "c++"
                ]
            }
        },
        "sort": [
            {"CommentCount": {"order": "desc"}}  # Sort by CommentCount (or adjust to 'Score' if needed)
        ],
        "_source": ["Body", "CommentCount", "OwnerUserId"]  # Specify the fields to retrieve
    }
    )
    return resp

#Query 10
#Search for comments that have the words Python and Sql within a 3 word range in the text and order them by score
def query10_os(client):
    resp = client.search(
    index="comments",  # Replace with your actual index name
    body={
        "query": {
            "bool": {
                "must": [
                    {
                        "match_phrase": {
                            "Text": {
                                "query": "sql python",  # Match 'sql' and 'python' in 'text'
                                "slop": 3  # Allow up to 3 positions between 'sql' and 'python'
                            }
                        }
                    }
                ]
            }
        },
        "_source": ["id", "Score"],  # Retrieve 'id' and 'Score'
        "sort": [
            {"Score": {"order": "desc"}}  # Sort by Score in descending order
        ]
    }
    )
    return resp

#Query 11
#Search for posts that have any 2 lenguages of programmation and order them by score
def query11_os(client):
    resp = client.search(
    index="comments",
    body={
        "size": 20,  # Retrieve top 20 results
        "query": {
            "bool": {
                "should": [
                    {"bool": {"must": [{"match": {"Text": "sql"}}, {"match": {"Text": "python"}}]}},
                    {"bool": {"must": [{"match": {"Text": "sql"}}, {"match": {"Text": "c++"}}]}},
                    {"bool": {"must": [{"match": {"Text": "sql"}}, {"match": {"Text": "r"}}]}},
                    {"bool": {"must": [{"match": {"Text": "sql"}}, {"match": {"Text": "ruby"}}]}},
                    {"bool": {"must": [{"match": {"Text": "sql"}}, {"match": {"Text": "php"}}]}},
                    {"bool": {"must": [{"match": {"Text": "sql"}}, {"match": {"Text": "java"}}]}},
                    {"bool": {"must": [{"match": {"Text": "sql"}}, {"match": {"Text": "javascript"}}]}},
                    {"bool": {"must": [{"match": {"Text": "python"}}, {"match": {"Text": "c++"}}]}},
                    {"bool": {"must": [{"match": {"Text": "python"}}, {"match": {"Text": "r"}}]}},
                    {"bool": {"must": [{"match": {"Text": "python"}}, {"match": {"Text": "ruby"}}]}},
                    {"bool": {"must": [{"match": {"Text": "python"}}, {"match": {"Text": "php"}}]}},
                    {"bool": {"must": [{"match": {"Text": "python"}}, {"match": {"Text": "java"}}]}},
                    {"bool": {"must": [{"match": {"Text": "python"}}, {"match": {"Text": "javascript"}}]}},
                    {"bool": {"must": [{"match": {"Text": "c++"}}, {"match": {"Text": "r"}}]}},
                    {"bool": {"must": [{"match": {"Text": "c++"}}, {"match": {"Text": "ruby"}}]}},
                    {"bool": {"must": [{"match": {"Text": "c++"}}, {"match": {"Text": "php"}}]}},
                    {"bool": {"must": [{"match": {"Text": "c++"}}, {"match": {"Text": "java"}}]}},
                    {"bool": {"must": [{"match": {"Text": "c++"}}, {"match": {"Text": "javascript"}}]}},
                    {"bool": {"must": [{"match": {"Text": "r"}}, {"match": {"Text": "ruby"}}]}},
                    {"bool": {"must": [{"match": {"Text": "r"}}, {"match": {"Text": "php"}}]}},
                    {"bool": {"must": [{"match": {"Text": "r"}}, {"match": {"Text": "java"}}]}},
                    {"bool": {"must": [{"match": {"Text": "r"}}, {"match": {"Text": "javascript"}}]}},
                    {"bool": {"must": [{"match": {"Text": "ruby"}}, {"match": {"Text": "php"}}]}},
                    {"bool": {"must": [{"match": {"Text": "ruby"}}, {"match": {"Text": "java"}}]}},
                    {"bool": {"must": [{"match": {"Text": "ruby"}}, {"match": {"Text": "javascript"}}]}},
                    {"bool": {"must": [{"match": {"Text": "php"}}, {"match": {"Text": "java"}}]}},
                    {"bool": {"must": [{"match": {"Text": "php"}}, {"match": {"Text": "javascript"}}]}},
                    {"bool": {"must": [{"match": {"Text": "java"}}, {"match": {"Text": "javascript"}}]}}
                ]
            }
        },
        "sort": [{"Score": {"order": "desc"}}],  # Sort by Score descending
        "_source": ["Id", "Score"]  # Retrieve only `Id` and `Score` fields
    }
    )
    return resp


#Query 12
#Search for users that have the word python or sql in the first 50 words of their AboutMe  and location is USA
def query12_os(client):
    resp = client.search(
    index="users",  # Replace with your actual index name
    body={
        "query": {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {"match": {"AboutMe": "python"}},  # Match 'python' in 'AboutMe'
                                {"match": {"AboutMe": "sql"}}  # Match 'sql' in 'AboutMe'
                            ]
                        }
                    },
                    {
                        "match": {"Location": "USA"}  # Match 'USA' in 'location'
                    }
                ]
            }
        },
        "_source": ["id"]  # Retrieve only the 'id' field
    }
    )
    return resp


#Query 13
# Query that counts how many times are mentioned this programming languages on the posts (Sql, python, R, Java, JavaScript, C++, Ruby, PHP)
def query13_os(client):
    resp = client.search(
    index='posts',
    body={
        "size": 0,  # We're aggregating, not fetching individual documents
        "query": {
            "bool": {
                "should": [
                    {"match_phrase": {"Body": "sql"}},
                    {"match_phrase": {"Body": "python"}},
                    {"match_phrase": {"Body": " R "}},
                    {"match_phrase": {"Body": "java"}},
                    {"match_phrase": {"Body": "javascript"}},
                    {"match_phrase": {"Body": "c++"}},
                    {"match_phrase": {"Body": "ruby"}},
                    {"match_phrase": {"Body": "php"}}
                ]
            }
        },
        "aggs": {
            "Programming_Language": {
                "filters": {
                    "filters": {
                        "SQL": {"match_phrase": {"Body": "sql"}},
                        "Python": {"match_phrase": {"Body": "python"}},
                        "R": {"match_phrase": {"Body": " R "}},
                        "Java": {"match_phrase": {"Body": "java"}},
                        "JavaScript": {"match_phrase": {"Body": "javascript"}},
                        "C++": {"match_phrase": {"Body": "c++"}},
                        "Ruby": {"match_phrase": {"Body": "ruby"}},
                        "PHP": {"match_phrase": {"Body": "php"}}
                    }
                }
            }
        }
    }
    )
    return resp


#Query 14
# Query that counts how many times are mentioned this programming languages on comments (Sql, python, R, Java, JavaScript, C++, Ruby, PHP)
def query14_os(client):
    resp = client.search(
    index='comments',
    body={
        "size": 0,  # We're aggregating, not fetching individual documents
        "query": {
            "bool": {
                "should": [
                    {"match_phrase": {"Text": "sql"}},
                    {"match_phrase": {"Text": "python"}},
                    {"match_phrase": {"Text": " R "}},
                    {"match_phrase": {"Text": "java"}},
                    {"match_phrase": {"Text": "javascript"}},
                    {"match_phrase": {"Text": "c++"}},
                    {"match_phrase": {"Text": "ruby"}},
                    {"match_phrase": {"Text": "php"}}
                ]
            }
        },
        "aggs": {
            "Programming_Language": {
                "filters": {
                    "filters": {
                        "SQL": {"match_phrase": {"Text": "sql"}},
                        "Python": {"match_phrase": {"Text": "python"}},
                        "R": {"match_phrase": {"Text": " R "}},
                        "Java": {"match_phrase": {"Text": "java"}},
                        "JavaScript": {"match_phrase": {"Text": "javascript"}},
                        "C++": {"match_phrase": {"Text": "c++"}},
                        "Ruby": {"match_phrase": {"Text": "ruby"}},
                        "PHP": {"match_phrase": {"Text": "php"}}
                    }
                }
            }
        }
    }   
    )
    return resp

#Query 15
# Count how many users wrote sql in their about me and wrote a comment with the word python. If they also have the word c++ in the comment rank it higher. Order by count and weight (count of comment weight uses of c++)
def query15_os(client):
    resp = client.search(
    index="commentsjoinusers",  # Replace with your actual index name
    body={
        "size": 0,  # We only need aggregated results
        "query": {
            "bool": {
                "must": [
                    {"match": {"AboutMe": "sql"}},  # Match 'sql' in 'AboutMe'
                    {"match": {"Text": "python"}}  # Match 'python' in 'Text'
                ],
                "should": [
                    {"match": {"Text": "c++"}}  # Optional match 'c++'
                ],
                "minimum_should_match": 0  # Include all documents regardless of 'c++'
            }
        },
        "aggs": {
            "user_groups": {
                "terms": {
                    "field": "UserId",  # Group by UserId
                    "size": 20,  # Top 20 users
                    "order": {"_count": "desc"}  # Order by count descending
                },
                "aggs": {
                    "weight_score": {
                        "top_hits": {
                            "_source": ["UserId"],  # Include UserId in results
                            "size": 1  # Top hit per group
                        }
                    }
                }
            }
        }
    }
    )
    return resp

#Query 16
# Search for AccountId, Age, EmailHash, Reputation of users that dont live in the USA and posted something where the body AND title has the word sql OR (python or php) (Note both have to have a word at least) and the name of the user AND the last editor name is Michael
def query16_os(client):
    resp = client.search(
    index="postsjoinusers",  # Replace with your actual index name
    body={
        "query": {
            "bool": {
                "must": [
                    # Match 'sql' in either 'Body' or 'Title'
                    {
                        "multi_match": {
                            "query": "sql",
                            "fields": ["Body", "Title"]
                        }
                    },
                    # Match 'Michael' in either 'LastEditorDisplayName' or 'DisplayName'
                    {
                        "multi_match": {
                            "query": "Michael",
                            "fields": ["LastEditorDisplayName", "DisplayName"]
                        }
                    }
                ],
                "should": [
                    # Match 'python' or 'php' in 'Body' or 'Title'
                    {
                        "multi_match": {
                            "query": "python",
                            "fields": ["Body", "Title"]
                        }
                    },
                    {
                        "multi_match": {
                            "query": "php",
                            "fields": ["Body", "Title"]
                        }
                    }
                ],
                "must_not": [
                    # Exclude 'USA' in the 'Location' field
                    {
                        "match": {"Location": "USA"}
                    }
                ],
                "minimum_should_match": 1  # Ensure at least one 'should' clause matches
            }
        },
        "_source": ["AccountId", "Age", "EmailHash", "Reputation"],  # Retrieve relevant fields
        "size": 20  # Adjust as needed for the number of results
    }
    )
    return resp

#Query 17
# Search for reputation of users that have posted any post with two prog. lenguages and a title starting with sql or ending with python and which reputation is over 150
def query17_os(client):
    resp = client.search(
    index="postsjoinusers",
    body={
        "query": {
            "bool": {
                 "should": [
                    {"match_phrase": {"Text": "sql"}},
                    {"match_phrase": {"Text": "python"}},
                    {"match_phrase": {"Text": " R "}},
                    {"match_phrase": {"Text": "java"}},
                    {"match_phrase": {"Text": "javascript"}},
                    {"match_phrase": {"Text": "c++"}},
                    {"match_phrase": {"Text": "ruby"}},
                    {"match_phrase": {"Text": "php"}}
                ],
                "must": [
                    {"range": {"Reputation": {"gt": 150}}}
                ]
            }
        },
        "_source": ["AccountId", "Reputation", "Body", "Title"],
        "size": 20
    }
    )
    return resp

#Query 18
# Search for users that commented sql and python with two words in between and whose age is over 18 or the have more than 10 Downvotes
def query18_os(client):
    resp = client.search(
        index="commentsjoinusers",  # Replace with your actual index name
        body={
            "query": {
                "bool": {
                    "must": [
                        {
                            
                            "match_phrase": {
                                "Text": {
                                    "query": "sql python",  # Match 'sql' and 'python' in 'text'
                                    "slop": 2  # Allow up to 3 positions between 'sql' and 'python'
                                }
                            }
                        }
                    ],
                    "filter": [
                        {
                            "bool": {
                                "should": [
                                    {"range": {"Age": {"gt": 18}}},  # Age > 18
                                    {"range": {"DownVotes": {"gt": 10}}}  # DownVotes > 10
                                ],
                                "minimum_should_match": 1  # At least one of the conditions must match
                            }
                        }
                    ]
                }
            },
            "_source": ["UserId", "Age", "DownVotes"],  # Retrieve relevant fields
            "size": 20  # Adjust as needed to limit the number of results
        }
    )
    return resp

queries_os = [
    query1_os, query2_os, query3_os, query4_os, query5_os,
    query6_os, query7_os, query8_os, query9_os, query10_os,
    query11_os, query12_os, query13_os, query14_os, query15_os,
    query16_os, query17_os, query18_os
]










