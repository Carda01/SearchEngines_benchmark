#Query1
query_all_comments="""
select * from dbo.Comments;
"""

#Query2
query_all_badges="""
select * from dbo.Badges;
"""

#Query3
query_all_linktypes="""
select * from dbo.LinkTypes;
"""

#Query4
query_all_postlinks="""
select * from dbo.PostLinks
"""

#Query5
query_all_posts="""
select * from dbo.Posts
"""

#Query6
query_all_poststypes="""
select * from dbo.PostTypes
"""

#Query7
query_all_users="""
select * from dbo.Users
"""

#Query8
query_all_votes="""
select * from dbo.Votes
"""

#Query9
query_all_votetypes="""
select * from dbo.VoteTypes
"""

#Query10
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

#Query11
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
#Query12
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
#Query13
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

#Query14
# Query that counts how many times are mentioned this programming languages on the posts (Sql, python, R, Java, JavaScript, C++, Ruby, PHP) by users
query_prog_lang_user_posts= """
SELECT
    OwnerUserId,
    DisplayName,
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
JOIN 
    Users u
ON
    p.OwnerUserId = u.accountId
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
    DisplayName,
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

#Query 15
#Query to Get the Top 10 Most Active Users

query_top_active_users = """
SELECT TOP 10
    u.DisplayName, 
    COUNT(p.Id) AS Post_Count
FROM 
    Users u
JOIN 
    Posts p ON u.accountId = p.OwnerUserId
WHERE 
    p.PostTypeId = 1 -- Question posts
GROUP BY 
    u.DisplayName
ORDER BY 
    Post_Count DESC;
"""

#Query16
#Query to Get the Top 10 Most Voted Posts 
query_top_voted_posts = """
SELECT TOP 10
    p.Id, 
    p.Title, 
    COUNT(v.Id) AS Vote_Count
FROM 
    Posts p
JOIN 
    Votes v ON p.Id = v.PostId
GROUP BY 
    p.Id, p.Title
ORDER BY 
    Vote_Count DESC;
"""

# Query #17 
# Get all posts with their title, body, creation date, score, tags, associated post type, and user details.
query_all_posts_with_type_and_user = """
SELECT 
    p.Id AS PostId,
    p.Title,
    p.Body,
    p.CreationDate AS PostCreationDate,
    p.Score AS PostScore,
    p.Tags,
    pt.Type AS PostType,
    u.DisplayName AS UserDisplayName,
    u.Reputation AS UserReputation,
    u.Location AS UserLocation
FROM 
    Posts p
JOIN 
    PostTypes pt ON p.PostTypeId = pt.Id
JOIN 
    Users u ON p.OwnerUserId = u.Id
ORDER BY 
    p.CreationDate DESC;
"""

# Query #18
# Retrieves the top 5 posts with the highest number of comments.
query_top_5_posts_by_comments = """
SELECT TOP 5
    p.Id AS PostId,
    p.Title,
    COUNT(c.Id) AS CommentCount
FROM 
    Posts p
LEFT JOIN 
    Comments c ON p.Id = c.PostId
GROUP BY 
    p.Id, p.Title
ORDER BY 
    CommentCount DESC;
"""

# Query #19
# Count the number of votes per post type
query_vote_count_by_post_type = """
SELECT 
    pt.Type AS PostType,
    COUNT(v.Id) AS VoteCount
FROM 
    PostTypes pt
LEFT JOIN 
    Posts p ON p.PostTypeId = pt.Id
LEFT JOIN 
    Votes v ON v.PostId = p.Id
GROUP BY 
    pt.Type
ORDER BY 
    VoteCount DESC;
"""

# Query #20
# Get the most active users based on the number of posts they've made
query_most_active_users = """
SELECT TOP 10
    u.DisplayName,
    COUNT(p.Id) AS PostCount
FROM 
    Users u
JOIN 
    Posts p ON p.OwnerUserId = u.Id
GROUP BY 
    u.DisplayName
ORDER BY 
    PostCount DESC;
"""

# Query #21
# Get the top 5 posts based on score and comment count 
query_top_5_posts_by_score_and_comments = """
SELECT TOP 5
    p.Title,
    p.Score AS PostScore,
    COUNT(c.Id) AS CommentCount,
    c.Id AS CommentId
FROM 
    Posts p
LEFT JOIN 
    Comments c ON p.Id = c.PostId
GROUP BY 
    p.Id, p.Title, p.Score
ORDER BY 
    p.Score DESC, CommentCount DESC;
"""

# Query #22
# Get the most common vote types for posts
query_common_vote_types = """
SELECT 
    vt.Name AS VoteType,
    COUNT(v.Id) AS VoteCount
FROM 
    VoteTypes vt
JOIN 
    Votes v ON v.VoteTypeId = vt.Id
GROUP BY 
    vt.Name
ORDER BY 
    VoteCount DESC;
"""

# Query #23
# Get the most active users based on the number of posts they've made
query_most_active_users = """
SELECT TOP 10
    u.DisplayName,
    COUNT(p.Id) AS PostCount
FROM 
    Users u
JOIN 
    Posts p ON p.OwnerUserId = u.Id
GROUP BY 
    u.DisplayName
ORDER BY 
    PostCount DESC;
"""

# Query #24
# Get the top 10 users who have received the most votes
query_top_10_users_with_votes = """
SELECT TOP 10
    u.DisplayName,
    COUNT(v.Id) AS VoteCount
FROM 
    Users u
JOIN 
    Posts p ON u.accountId = p.OwnerUserId
JOIN 
    Votes v ON v.PostId = p.Id
GROUP BY 
    u.DisplayName
ORDER BY 
    VoteCount DESC;
"""

# Query #25
# Get the number of questions and answers for each user
query_questions_and_answers_by_user = """
SELECT 
    u.DisplayName,
    SUM(CASE WHEN p.PostTypeId = 1 THEN 1 ELSE 0 END) AS QuestionCount,
    SUM(CASE WHEN p.PostTypeId = 2 THEN 1 ELSE 0 END) AS AnswerCount
FROM 
    Users u
JOIN 
    Posts p ON p.OwnerUserId = u.Id
GROUP BY 
    u.DisplayName;
"""

# Query #26
# Get the top 5 most popular tags
query_top_5_popular_tags = """
SELECT TOP 5
    t.TagName,
    COUNT(pt.Id) AS PostCount
FROM 
    Tags t
JOIN 
    PostTags pt ON t.Id = pt.TagId
GROUP BY 
    t.TagName
ORDER BY 
    PostCount DESC;
"""

# Query #27
# Get the most active users based on the number of comments
query_most_active_users_by_comments = """
SELECT TOP 10
    u.DisplayName,
    COUNT(c.Id) AS CommentCount
FROM 
    Users u
JOIN 
    Comments c ON c.UserId = u.accountId
GROUP BY 
    u.DisplayName
ORDER BY 
    CommentCount DESC;
"""

# Query #28
# Get the top 10 most commented posts
query_top_10_most_commented_posts = """
SELECT TOP 10
    p.Title,
    COUNT(c.Id) AS CommentCount
FROM 
    Posts p
LEFT JOIN 
    Comments c ON p.Id = c.PostId
GROUP BY 
    p.Title
ORDER BY 
    CommentCount DESC;
"""

# Query #29
# Get the most upvoted and downvoted posts
query_upvotes_downvotes_per_post = """
SELECT 
    p.Title,
    SUM(CASE WHEN v.VoteTypeId = 2 THEN 1 ELSE 0 END) AS Upvotes,
    SUM(CASE WHEN v.VoteTypeId = 3 THEN 1 ELSE 0 END) AS Downvotes
FROM 
    Posts p
JOIN 
    Votes v ON p.Id = v.PostId
GROUP BY 
    p.Title
ORDER BY 
    Upvotes DESC, Downvotes DESC;
"""


## Dictionary of queries

query_dictionary = {
    'id':(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29),
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
                      query_prog_lang_user_posts,
                      query_top_active_users,
                      query_top_voted_posts,
                      query_all_posts_with_type_and_user,
                      query_top_5_posts_by_comments,
                      query_vote_count_by_post_type,
                      query_most_active_users,
                      query_top_5_posts_by_score_and_comments,
                      query_common_vote_types,
                      query_most_active_users,
                      query_top_10_users_with_votes,
                      query_questions_and_answers_by_user,
                      query_top_5_popular_tags,
                      query_most_active_users_by_comments,
                      query_top_10_most_commented_posts,
                      query_upvotes_downvotes_per_post
    ]
}
