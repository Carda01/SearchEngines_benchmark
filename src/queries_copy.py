#Query 1
#Search for comments that contain the word 'Python' and order them by their score.
query_1 = """
            SELECT TOP 20 id, Score
            FROM comments
            WHERE text LIKE '%python%'
            ORDER BY Score DESC;
            """
#Query 2
#Search for posts that contain the word 'Python' in the title, that have been closed and ordered by score 
query_2="""
            SELECT TOP 20 id, Score
            FROM posts 
            WHERE title LIKE '%python%' AND ClosedDate!=0
            ORDER BY Score DESC;
            """
#Query 3
#Search for users that contain the word 'Python' AND 'SQL' in the AboutMe and order by their reputation and last access date
query_3="""
            SELECT TOP 20 AccountId, Reputation, LastAccessDate
            FROM users
            WHERE (AboutMe LIKE '%python%' AND AboutMe LIKE '%sql%') AND (AboutMe LIKE '%java%' OR AboutMe LIKE '%javascript%')
            ORDER BY Reputation DESC, LastAccessDate DESC
"""

#Query 4
#Search for posts that contain the word 'Python' OR 'SQL' and that have more than 3 Favoirite counts
query_4="""
            SELECT TOP 20 id
            FROM posts
            WHERE (Body LIKE '%python%' OR Body LIKE '%sql%') AND FavoriteCount>3;
            """
#Query 5
#Search for comments that contain the word 'Python' BUT NOT 'SQL' created in 2008
query_5="""
            SELECT TOP 20 id, CreationDate
            FROM comments
            WHERE text LIKE '%python%' AND text NOT LIKE '%sql%' AND CreationDate LIKE '2008%' ;
            """

#Query 6
#Search for the users without downvotes that contain the word 'Python' OR 'SQL' in their AboutMe but double the value on the ranking of the word 'SQL'
#YOU CAN'T DO THIS (NO RANKING)
query_6=""

#Query 7
#Search for posts that their body start with the <p>, their title ends with sql and they contain the word sql in their tags
#DOESN'T WORK HAS PROBLEMS WITH WHITE SPACES
query_7="""
            SELECT TOP 20 *
            FROM posts 
            WHERE body LIKE '<p>%' AND title LIKE '%sql' AND tags LIKE '%sql%';
            """
            
#Query 8
#Search for users  who have in their about me Python and SQL but if they have any additional programming lenguage rank them higher, and display the weight of the ranking.
#Not weight function or MAYBE this is not possible
query_8=""
           
#Query 9
#Search for posts with python in the title, sql in the body and c++ in the tags and order them by score. 
query_9="""
            SELECT TOP 20 id, Score
            FROM posts 
            WHERE title LIKE '%python%' AND body LIKE '%sql%' AND tags LIKE '%c++%'
            ORDER BY Score DESC;
        """
#Query 10
#Search for comments that have the words Python and Sql within a 3 word range in the text and order them by score
#May be doable but no idea how
query_10=""

#Query 11
#Search for posts that have any 2 lenguages of programmation and order them by score
query_11="""   
            SELECT TOP 20 id, Score
            FROM comments
            WHERE
            (text LIKE '%sql%' AND text LIKE '%python%') OR
            (text LIKE '%sql%' AND text LIKE '%c++%') OR
            (text LIKE '%sql%' AND text LIKE '%r%') OR
            (text LIKE '%sql%' AND text LIKE '%ruby%') OR
            (text LIKE '%sql%' AND text LIKE '%php%') OR
            (text LIKE '%sql%' AND text LIKE '%java%') OR
            (text LIKE '%sql%' AND text LIKE '%javascript%') OR
            (text LIKE '%python%' AND text LIKE '%c++%') OR
            (text LIKE '%python%' AND text LIKE '%r%') OR
            (text LIKE '%python%' AND text LIKE '%ruby%') OR
            (text LIKE '%python%' AND text LIKE '%php%') OR
            (text LIKE '%python%' AND text LIKE '%java%') OR
            (text LIKE '%python%' AND text LIKE '%javascript%') OR
            (text LIKE '%c++%' AND text LIKE '%r%') OR
            (text LIKE '%c++%' AND text LIKE '%ruby%') OR
            (text LIKE '%c++%' AND text LIKE '%php%') OR
            (text LIKE '%c++%' AND text LIKE '%java%') OR
            (text LIKE '%c++%' AND text LIKE '%javascript%') OR
            (text LIKE '%r%' AND text LIKE '%ruby%') OR
            (text LIKE '%r%' AND text LIKE '%php%') OR
            (text LIKE '%r%' AND text LIKE '%java%') OR
            (text LIKE '%r%' AND text LIKE '%javascript%') OR
            (text LIKE '%ruby%' AND text LIKE '%php%') OR
            (text LIKE '%ruby%' AND text LIKE '%java%') OR
            (text LIKE '%ruby%' AND text LIKE '%javascript%') OR
            (text LIKE '%php%' AND text LIKE '%java%') OR
            (text LIKE '%php%' AND text LIKE '%javascript%') OR
            (text LIKE '%java%' AND text LIKE '%javascript%')
            ORDER BY Score DESC;           
        """

#Query 12
#Search for users that have the word python or sql in the first 50 words of their AboutMe  and location is USA
#You can't limitate the collumn Like search span
query_12 = ""


#Query 13
# Query that counts how many times are mentioned this programming languages on the posts (Sql, python, R, Java, JavaScript, C++, Ruby, PHP)
query_13 = """
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

#Query 14
# Query that counts how many times are mentioned this programming languages on comments (Sql, python, R, Java, JavaScript, C++, Ruby, PHP)


query_14 = """
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


## Dictionary of queries

query_dictionary = {}
for i in range(14):
    query_dictionary[i + 1] = globals()[f"query_{i+1}"]
