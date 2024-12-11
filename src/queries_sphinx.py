

##############################################################################################

#Query 1
#Search for comments that contain the word 'Python' and order them by their score.
query_1="""
            SELECT id, Score 
            FROM comments 
            WHERE MATCH('@text Python')
            ORDER BY Score DESC
            """
#Query 2
#Search for posts that contain the word 'Python' in the title, that have been closed and ordered by score 
query_2="""
            SELECT id, Score
            FROM posts 
            WHERE MATCH('@title Python') AND ClosedDate!=0
            ORDER BY Score DESC
            """
#Query 3
#Search for users that contain the word 'Python' AND 'SQL' AND 'Java' in the AboutMe and order by their reputation and last access date
query_3="""
            SELECT AccountId, Reputation, LastAccessDate 
            FROM users
            WHERE MATCH('@AboutMe Python SQL (Java | Javascript)')
            ORDER BY Reputation DESC, LastAccessDate DESC
"""

#Query 4
#Search for posts that contain the word 'Python' OR 'SQL' and that have more than 3 Favoirite counts
query_4="""
            SELECT id
            FROM posts 
            WHERE MATCH('@body Python | SQL') AND FavoriteCount>3
            """
#Query 5
#Search for comments that contain the word 'Python' BUT NOT 'SQL' created in 2008
query_5="""
            SELECT id, CreationDate
            FROM comments 
            WHERE MATCH('@text Python -SQL') AND CreationDate=2008
            """

#Query 6
#Search for the users without downvotes that contain the word 'Python' OR 'SQL' in their AboutMe but double the value on the ranking of the word 'SQL'
query_6="""
            SELECT id, DownVotes
            FROM users 
            WHERE MATCH('@AboutMe Python | SQL^2') and Downvotes=0
            ORDER BY DownVotes DESC   
            """
#Query 7
#Search for posts that their body start with the <p>, their title ends with sql and they contain the word sql in their tags
query_7="""
            SELECT *
            FROM posts 
            WHERE MATCH('@body ^<p> @title sql$ @tags sql')
            """
#Query 8
#Search for users  who have in their about me Python and SQL but if they have any additional programming lenguage rank them higher, and display the weight of the ranking.
query_8="""
            SELECT id, WEIGHT()
            FROM users
            WHERE MATCH('@aboutme python sql MAYBE ( c++ || r || ruby || php || java || javascript)')  
            """
#Query 9 
#Search for posts with python in the title, sql in the body and c++ in the tags and order them by score. 
query_9="""
            SELECT id, Score
            FROM posts 
            WHERE MATCH('@title python @body sql @tags c++')
            ORDER BY Score DESC
        """
#Query 10
#Search for comments that have the words Python and Sql within a 3 word range in the text and order them by score
query_10="""
            SELECT id, Score
            FROM comments
            WHERE MATCH('@text sql NEAR/3 python')
            ORDER BY Score DESC
        """
#Query 11
#Search for posts that have any 2 lenguages of programmation and order them by score
query_11="""   
            SELECT id, Score
            FROM comments
            WHERE MATCH('"sql python c++ r ruby php java javascript"/2')
            ORDER BY Score DESC               
        """

#Query 12
#Search for users that have the word python or sql in the first 50 words of their AboutMe  and location is USA
query_12 = """
            SELECT id
            FROM users 
            WHERE MATCH('@AboutMe[50] python | sql @location USA') 
"""


#Query 13
# Query that counts how many times are mentioned this programming languages on the posts (Sql, python, R, Java, JavaScript, C++, Ruby, PHP)
query_13 = "CALL KEYWORDS('sql python  R  java javascript c++ ruby php', 'posts', 1)"


#Query 14
# Query that counts how many times are mentioned this programming languages on comments (Sql, python, R, Java, JavaScript, C++, Ruby, PHP)

query_14 = "CALL KEYWORDS('sql python  R  java javascript c++ ruby php', 'comments', 1)"

query_15="""
            SELECT userid, count(*) as total, WEIGHT() 
            FROM usersjoincomments
            WHERE MATCH('@AboutMe sql @text python MAYBE c++')  
            GROUP BY userid
            ORDER BY total DESC, WEIGHT() DESC
            """
query_16="""
            SELECT AccountId, Age, EmailHash, Reputation
            FROM usersjoinposts
            WHERE MATCH('@Location !USA @(Body,Title) sql (python OR php)  @(LastEditorDisplayName,DisplayName) Michael')
            """

query_17="""
            SELECT AccountId, Reputation
            FROM usersjoinposts
            WHERE MATCH('@Body "sql python c++ r ruby php java javascript"/2 @Title ^sql | python$') 
            AND Reputation > 150
            """
query_18="""      
            SELECT userid, (Age>18 OR DownVotes>10) AS cond, WEIGHT() 
            FROM usersjoincomments
            WHERE MATCH('@text "sql * * python"') 
            AND cond=1
            """
## Dictionary of queries

query_dictionary = {}
for i in range(18):
    query_dictionary[i + 1] = globals()[f"query_{i+1}"]



