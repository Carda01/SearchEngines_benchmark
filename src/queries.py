query_all_comments="""
select * from dbo.Comments;
"""

query_all_badges="""
select * from dbo.Badges;
"""

query_all_linktypes="""
select * from dbo.LinkTypes;
"""

query_all_postlinks="""
select * from dbo.PostLinks
"""

query_all_posts="""
select * from dbo.Posts
"""

query_all_poststypes="""
select * from dbo.PostTypes
"""

query_all_users="""
select * from dbo.Users
"""

query_all_votes="""
select * from dbo.Votes
"""

query_all_votetypes="""
select * from dbo.VoteTypes
"""

# Query that counts how many times are mentioned this programming languages on comments (Sql, python, R, Java, JavaScript, C++, Ruby, PHP)

query_prog_lang_comments = """
SELECT 
    CASE
        WHEN Text LIKE '%sql%' THEN 'SQL'
        WHEN Text LIKE '%python%' THEN 'Python'
        WHEN Text LIKE '% R %' THEN 'R'
        WHEN Text LIKE '%java%' THEN 'Java'
        WHEN Text LIKE '%javascript%' THEN 'JavaScript'
        WHEN Text LIKE '%c++%' THEN 'C++'
        WHEN Text LIKE '%ruby%' THEN 'Ruby'
        WHEN Text LIKE '%php%' THEN 'PHP'
        ELSE 'Other'
    END AS Programming_Language,
    COUNT(*) AS Post_Count
FROM 
    comments
WHERE 
    Text LIKE '%sql%' 
    OR Text LIKE '%python%' 
    OR Text LIKE '% R %'
    OR Text LIKE '%java%' 
    OR Text LIKE '%javascript%' 
    OR Text LIKE '%c++%' 
    OR Text LIKE '%ruby%' 
    OR Text LIKE '%php%' 
GROUP BY 
    CASE
        WHEN Text LIKE '%sql%' THEN 'SQL'
        WHEN Text LIKE '%python%' THEN 'Python'
        WHEN Text LIKE '% R %' THEN 'R'
        WHEN Text LIKE '%java%' THEN 'Java'
        WHEN Text LIKE '%javascript%' THEN 'JavaScript'
        WHEN Text LIKE '%c++%' THEN 'C++'
        WHEN Text LIKE '%ruby%' THEN 'Ruby'
        WHEN Text LIKE '%php%' THEN 'PHP'
        ELSE 'Other'
    END;
"""
# Query that counts how many times are mentioned this programming languages (Sql, python, R, Java, JavaScript, C++, Ruby, PHP) by user
# It makes a JOIN with the user table
query_prog_lang_user_comments = """
SELECT 
    UserId,
    DisplayName,
    CASE
        WHEN Text LIKE '%sql%' THEN 'SQL'
        WHEN Text LIKE '%python%' THEN 'Python'
        WHEN Text LIKE '% r %' THEN 'R'
        WHEN Text LIKE '%java%' THEN 'Java'
        WHEN Text LIKE '%javascript%' THEN 'JavaScript'
        WHEN Text LIKE '%c++%' THEN 'C++'
        WHEN Text LIKE '%ruby%' THEN 'Ruby'
        WHEN Text LIKE '%php%' THEN 'PHP'
        ELSE 'Other'
    END AS Programming_Language,
    COUNT(*) AS Post_Count
FROM 
    comments c
JOIN 
    Users u
ON
    c.UserId = u.accountId
WHERE 
    Text LIKE '%sql%' 
    OR Text LIKE '%python%' 
    OR Text LIKE '% r %'
    OR Text LIKE '%java%' 
    OR Text LIKE '%javascript%' 
    OR Text LIKE '%c++%' 
    OR Text LIKE '%ruby%' 
    OR Text LIKE '%php%' 
GROUP BY 
    UserId,
    DisplayName,
    CASE
        WHEN Text LIKE '%sql%' THEN 'SQL'
        WHEN Text LIKE '%python%' THEN 'Python'
        WHEN Text LIKE '% r %' THEN 'R'
        WHEN Text LIKE '%java%' THEN 'Java'
        WHEN Text LIKE '%javascript%' THEN 'JavaScript'
        WHEN Text LIKE '%c++%' THEN 'C++'
        WHEN Text LIKE '%ruby%' THEN 'Ruby'
        WHEN Text LIKE '%php%' THEN 'PHP'
        ELSE 'Other'
    END
ORDER BY UserId;
"""
# Query that counts the Top 20 common words in comments without considering stop words
query_top_20_words_comments = """
SELECT TOP 20 
    value AS Word, 
    COUNT(*) AS Frequency
FROM 
    comments
CROSS APPLY 
    STRING_SPLIT(Text, ' ') -- Split by spaces
WHERE 
    value NOT IN (
        'the', 'and', 'is', 'a', 'of', 'to', 'in', 'that', 'it', 'on', 'for', 'with', 'as', 'at', 
        'this', 'by', 'an', 'be', 'or', 'from', 'but', 'not', 'are', 'were', 'have', 'has', 'had', 
        'I', 'you', 'they', 'we', 'he', 'she', 'them', 'his', 'her', 'hers', 'its', 'our', 'ours', 
        'your', 'yours', 'my', 'mine', 'me', 'us', 'him', 'her', 'ourselves', 'theirs', 'who', 
        'whom', 'which', 'what', 'where', 'when', 'why', 'how', 'all', 'any', 'some', 'one', 'two', 
        'three', 'each', 'every', 'few', 'more', 'most', 'least', 'much', 'many', 'several', 'whoever', 
        'whenever', 'whatever', 'whichever', 'no', 'nor', 'not', 'so', 'than', 'too', 'very', 's', 't', 
        'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 
        'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 
        'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', 'here', 'there', 'when', 'where', 
        'how', 'why', 'which', 'what', 'can', 'could', 'would', 'might', 'should', 'must', 'shall', 
        'ought', 'be', 'being', 'been', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 
        'themselves', 'yourselves', 'both', 'either', 'neither', 'each', 'every', 'many', 'few', 'less', 
        'least', 'fewest', 'more', 'most', 'least', 'quite', 'some', 'any', 'all', 'such', 'noone', 'none', 
        'nothing', 'neither', 'no', 'nor', 'not', 'cannot', 'without', 'within', 'against', 'under', 'over',
        'along', 'before', 'after', 'during', 'between', 'through', 'above', 'below', 'if', 'use', 'was', '-', 
        'like', 'dont', 'using', 'Im', 'it''s', 'i''m', 'don''t','need', 'think', 'only', 'get', 'then', 'want', 'answer', 'question',
        'because', 'also', 'you''re', 'question', 'out', 'good'
    ) -- Filter more common stop words
    AND value != '' -- Exclude empty strings
GROUP BY 
    value
ORDER BY 
    Frequency DESC;
"""
# Query that counts how many times are mentioned this programming languages on the posts (Sql, python, R, Java, JavaScript, C++, Ruby, PHP)
query_prog_lang_posts = """
SELECT 
    CASE
        WHEN Body LIKE '%sql%' THEN 'SQL'
        WHEN Body LIKE '%python%' THEN 'Python'
        WHEN Body LIKE '% R %' THEN 'R'
        WHEN Body LIKE '%java%' THEN 'Java'
        WHEN Body LIKE '%javascript%' THEN 'JavaScript'
        WHEN Body LIKE '%c++%' THEN 'C++'
        WHEN Body LIKE '%ruby%' THEN 'Ruby'
        WHEN Body LIKE '%php%' THEN 'PHP'
        ELSE 'Other'
    END AS Programming_Language,
    COUNT(*) AS Post_Count
FROM 
    posts
WHERE 
    Body LIKE '%sql%' 
    OR Body LIKE '%python%' 
    OR Body LIKE '% R %'
    OR Body LIKE '%java%' 
    OR Body LIKE '%javascript%' 
    OR Body LIKE '%c++%' 
    OR Body LIKE '%ruby%' 
    OR Body LIKE '%php%' 
GROUP BY 
    CASE
        WHEN Body LIKE '%sql%' THEN 'SQL'
        WHEN Body LIKE '%python%' THEN 'Python'
        WHEN Body LIKE '% R %' THEN 'R'
        WHEN Body LIKE '%java%' THEN 'Java'
        WHEN Body LIKE '%javascript%' THEN 'JavaScript'
        WHEN Body LIKE '%c++%' THEN 'C++'
        WHEN Body LIKE '%ruby%' THEN 'Ruby'
        WHEN Body LIKE '%php%' THEN 'PHP'
        ELSE 'Other'
    END
ORDER BY
    Post_Count;
"""

# Query that counts how many times are mentioned this programming languages on the posts (Sql, python, R, Java, JavaScript, C++, Ruby, PHP) by users
query_prog_lang_user_posts= """
SELECT
    OwnerUserId,
    CASE
        WHEN Body LIKE '%sql%' THEN 'SQL'
        WHEN Body LIKE '%python%' THEN 'Python'
        WHEN Body LIKE '% R %' THEN 'R'
        WHEN Body LIKE '%java%' THEN 'Java'
        WHEN Body LIKE '%javascript%' THEN 'JavaScript'
        WHEN Body LIKE '%c++%' THEN 'C++'
        WHEN Body LIKE '%ruby%' THEN 'Ruby'
        WHEN Body LIKE '%php%' THEN 'PHP'
        ELSE 'Other'
    END AS Programming_Language,
    COUNT(*) AS Post_Count
FROM 
    posts p
WHERE 
    Body LIKE '%sql%' 
    OR Body LIKE '%python%' 
    OR Body LIKE '% R %'
    OR Body LIKE '%java%' 
    OR Body LIKE '%javascript%' 
    OR Body LIKE '%c++%' 
    OR Body LIKE '%ruby%' 
    OR Body LIKE '%php%' 
GROUP BY
    OwnerUserId,
    CASE
        WHEN Body LIKE '%sql%' THEN 'SQL'
        WHEN Body LIKE '%python%' THEN 'Python'
        WHEN Body LIKE '% R %' THEN 'R'
        WHEN Body LIKE '%java%' THEN 'Java'
        WHEN Body LIKE '%javascript%' THEN 'JavaScript'
        WHEN Body LIKE '%c++%' THEN 'C++'
        WHEN Body LIKE '%ruby%' THEN 'Ruby'
        WHEN Body LIKE '%php%' THEN 'PHP'
        ELSE 'Other'
    END
ORDER BY
    Post_Count;
"""

## Dictionary of queries

query_dictionary = {
    'id':(1,2,3,4,5,6,7,8,9,10,11,12,13,14),
    'query':[query_all_comments,
                      query_all_badges,
                      query_all_linktypes,
                      query_all_postlinks,
                      query_all_posts,
                      query_all_poststypes,
                      query_all_users,
                      query_all_votes,
                      query_all_votetypes,
                      query_prog_lang_comments,
                      query_prog_lang_user_comments,
                      query_top_20_words_comments,
                      query_prog_lang_posts,
                      query_prog_lang_user_posts
    ]
}

