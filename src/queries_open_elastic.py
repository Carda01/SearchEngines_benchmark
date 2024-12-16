#Query 1
#Search for comments that contain the word 'Python' and order them by their score.
def query1(client,scale):
    resp = client.search(
    index=f"comments_{scale}",
    body={
            "size": 20,
            "query": {
                "match": {
                    "Text": "python"  
                }
            },
            "_source": ["id", "Score"],  
            "sort": [
                {"Score": {"order": "desc"}}  
            ]
        }
    )
    return resp

#Query 2
#Search for posts that contain the word 'Python' in the title, that have been closed and ordered by score 
def query2(client,scale):
    resp = client.search(
    index=f"posts_{scale}",  
    body={
        "size": 20,  
        "query": {
            "bool": {
                "must": [
                    {"match": {"Title": "python"}}  
                ],
                "filter": [
                    {"exists": {"field": "ClosedDate"}},  
                    {"range": {
                        "ClosedDate": {
                            "lt": '2070-01-01 00:00:00.000'  
                        }
                    }}
                ]
            }
        },
        "_source": ["id", "Score"],  
        "sort": [
            {"Score": {"order": "desc"}}  
        ]
    }
)
    return resp


#Query 3
#Search for users that contain the word 'Python' AND 'SQL' AND 'Java' in the AboutMe and order by their reputation and last access date
def query3(client, scale):
    resp = client.search(
    index=f"users_{scale}",  
    body={
        "size": 20,  
        "query": {
            "bool": {
                "must": [
                    {"match": {"AboutMe": "python"}},  
                    {"match": {"AboutMe": "sql"}}     
                ],
                "should": [
                    {"match": {"AboutMe": "java"}},    
                    {"match": {"AboutMe": "javascript"}}  
                ],
                "minimum_should_match": 1  
            }
        },
        "_source": ["AccountId", "Reputation", "LastAccessDate"],  
        "sort": [
            {"Reputation": {"order": "desc"}},  
            {"LastAccessDate": {"order": "desc"}}  
        ]
    }
    )
    return resp


#Query 4
#Search for posts that contain the word 'Python' OR 'SQL' and that have more than 3 Favoirite counts
def query4(client, scale):
    resp = client.search(
    index=f"posts_{scale}",  
    body={
        "size": 20,  
        "query": {
            "bool": {
                "must": [
                    {"range": {"FavoriteCount": {"gt": 3}}}  
                ],
                "should": [
                    {"match": {"Body": "python"}},  
                    {"match": {"Body": "sql"}}  
                ],
                "minimum_should_match": 1  
            }
        },
        "_source": ["id"]  
    }
    )
    return resp

#Query 5
#Search for comments that contain the word 'Python' BUT NOT 'SQL' created in 2008
def query5(client, scale):
    resp = client.search(
    index=f"comments_{scale}",  
    body={
        "size": 20,  
        "query": {
            "bool": {
                "must": [
                    {"match": {"Text": "python"}},  
                ],
                "must_not": [
                    {"match": {"Text": "sql"}},  
                ],
                "filter": [
                    {"range": {
                        "CreationDate": {
                            "gte": "2008-01-01 00:00:00.000",  
                            "lt": "2009-01-01 00:00:00.000"  
                        }
                    }}
                ]
            }
        },
        "_source": ["id", "CreationDate"]  
    }
    )
    return resp

#Query 6
#Search for the users without downvotes that contain the word 'Python' OR 'SQL' in their AboutMe but double the value on the ranking of the word 'SQL'
def query6(client, scale):
    resp = client.search(
    index=f"users_{scale}",  
    body={
        "query": {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {"match": {"AboutMe": "Python"}},  
                                {"match": {"AboutMe": "SQL"}}     
                            ],
                            "minimum_should_match": 1  
                        }
                    }
                ],
                "filter": [
                    {"term": {"DownVotes": 0}}  
                ]
            }
        },
        "_source": ["id", "DownVotes"],  
        "sort": [
            {"DownVotes": {"order": "desc"}}  
        ]
    }
    )
    return resp

#Query 7
#Search for posts that their body start with the <p>, their title ends with sql and they contain the word sql in their tags
def query7(client,scale):
    resp = client.search(
    index=f"posts_{scale}",
    body={
        "size": 20,  
        "query": {
            "bool": {
                "must": [
                    {"match": {"Body": "<p>"}},
                    {"match": {"Title": "sql"}},
                    {"match": {"Tags":"sql"}}
                ]
            }
        },
        
        "_source": ["Body", "Title", "Tags", "Score"]
    }
    )
    return resp


#Query 8
#Search for users  who have in their about me Python and SQL but if they have any additional programming lenguage rank them higher, and display the weight of the ranking.
def query8(client, scale):
    resp = client.search(
    index=f"users_{scale}",  
    body={
        "query": {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {"match": {"AboutMe": "python"}},  
                                {"match": {"AboutMe": "sql"}},    
                                {
                                    "bool": {
                                        "should": [
                                            {"match": {"AboutMe": "c++"}},  
                                            {"match": {"AboutMe": "r"}},    
                                            {"match": {"AboutMe": "ruby"}}, 
                                            {"match": {"AboutMe": "php"}},  
                                            {"match": {"AboutMe": "java"}}, 
                                            {"match": {"AboutMe": "javascript"}} 
                                        ]
                                    }
                                }
                            ],
                            "minimum_should_match": 1  
                        }
                    }
                ]
            }
        },
        "_source": ["id"],  
    }
    )
    return resp

#Query 9 
#Search for posts with python in the title, sql in the body and c++ in the tags and order them by score. 
def query9(client, scale):
    resp = client.search(
    index=f"posts_{scale}",
    body={
        "size": 20,  
        "query": {
            "bool": {
                "must": [  
                    {"match": {"Body": "sql"}},  
                    {"match": {"Body": "python"}},  
                    {"match": {"Body": "c++"}}  
                ]
            }
        },
        "sort": [
            {"CommentCount": {"order": "desc"}}  
        ],
        "_source": ["Body", "CommentCount", "OwnerUserId"]  
    }
    )
    return resp

#Query 10
#Search for comments that have the words Python and Sql within a 3 word range in the text and order them by score
def query10(client,scale):
    resp = client.search(
    index=f"comments_{scale}",  
    body={
        "query": {
            "bool": {
                "must": [
                    {
                        "match_phrase": {
                            "Text": {
                                "query": "sql python",  
                                "slop": 3  
                            }
                        }
                    }
                ]
            }
        },
        "_source": ["id", "Score"],  
        "sort": [
            {"Score": {"order": "desc"}}  
        ]
    }
    )
    return resp

#Query 11
#Search for posts that have any 2 lenguages of programmation and order them by score
def query11(client, scale):
    resp = client.search(
    index=f"comments_{scale}",
    body={
        "size": 20,  
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
        "sort": [{"Score": {"order": "desc"}}],  
        "_source": ["Id", "Score"]  
    }
    )
    return resp


#Query 12
#Search for users that have the word python or sql in the first 50 words of their AboutMe  and location is USA
def query12(client,scale):
    resp = client.search(
    index=f"users_{scale}", 
    body={
        "query": {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {"match": {"AboutMe": "python"}},  
                                {"match": {"AboutMe": "sql"}}  
                            ]
                        }
                    },
                    {
                        "match": {"Location": "USA"}  
                    }
                ]
            }
        },
        "_source": ["id"]  
    }
    )
    return resp


#Query 13
# Query that counts how many times are mentioned this programming languages on the posts (Sql, python, R, Java, JavaScript, C++, Ruby, PHP)
def query13(client,scale):
    resp = client.search(
    index=f'posts_{scale}',
    body={
        "size": 0,  
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
def query14(client,scale):
    resp = client.search(
    index=f'comments_{scale}',
    body={
        "size": 0,  
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
def query15(client, scale):
    resp = client.search(
    index=f"commentsjoinusers_{scale}",  
    body={
        "size": 0,  
        "query": {
            "bool": {
                "must": [
                    {"match": {"AboutMe": "sql"}},  
                    {"match": {"Text": "python"}}  
                ],
                "should": [
                    {"match": {"Text": "c++"}}  
                ],
                "minimum_should_match": 0  
            }
        },
        "aggs": {
            "user_groups": {
                "terms": {
                    "field": "UserId",  
                    "size": 20,  
                    "order": {"_count": "desc"}  
                },
                "aggs": {
                    "weight_score": {
                        "top_hits": {
                            "_source": ["UserId"],  
                            "size": 1  
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
def query16(client, scale):
    resp = client.search(
    index=f"postsjoinusers_{scale}",  
    body={
        "query": {
            "bool": {
                "must": [
                    
                    {
                        "multi_match": {
                            "query": "sql",
                            "fields": ["Body", "Title"]
                        }
                    },
                    
                    {
                        "multi_match": {
                            "query": "Michael",
                            "fields": ["LastEditorDisplayName", "DisplayName"]
                        }
                    }
                ],
                "should": [
                    
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
                    
                    {
                        "match": {"Location": "USA"}
                    }
                ],
                "minimum_should_match": 1  
            }
        },
        "_source": ["AccountId", "Age", "EmailHash", "Reputation"],  
        "size": 20  
    }
    )
    return resp

#Query 17
# Search for reputation of users that have posted any post with two prog. lenguages and a title starting with sql or ending with python and which reputation is over 150
def query17(client, scale):
    resp = client.search(
    index=f"postsjoinusers_{scale}",
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
def query18(client, scale):
    resp = client.search(
        index=f"commentsjoinusers_{scale}",
        body={
            "query": {
                "bool": {
                    "must": [
                        {
                            
                            "match_phrase": {
                                "Text": {
                                    "query": "sql python",
                                    "slop": 2  
                                }
                            }
                        }
                    ],
                    "filter": [
                        {
                            "bool": {
                                "should": [
                                    {"range": {"Age": {"gt": 18}}},  
                                    {"range": {"DownVotes": {"gt": 10}}}  
                                ],
                                "minimum_should_match": 1  
                            }
                        }
                    ]
                }
            },
            "_source": ["UserId", "Age", "DownVotes"],  
            "size": 20  
        }
    )
    return resp

queries = [
    lambda client, scale: query1(client, scale),
    lambda client, scale: query2(client, scale),
    lambda client, scale: query3(client, scale),
    lambda client, scale: query4(client, scale),
    lambda client, scale: query5(client, scale),
    lambda client, scale: query6(client, scale),
    lambda client, scale: query7(client, scale),
    lambda client, scale: query8(client, scale),
    lambda client, scale: query9(client, scale),
    lambda client, scale: query10(client, scale),
    lambda client, scale: query11(client, scale),
    lambda client, scale: query12(client, scale),
    lambda client, scale: query13(client, scale),
    lambda client, scale: query14(client, scale),
    lambda client, scale: query15(client, scale),
    lambda client, scale: query16(client, scale),
    lambda client, scale: query17(client, scale),
    lambda client, scale: query18(client, scale)
]
