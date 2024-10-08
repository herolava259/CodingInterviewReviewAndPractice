USE SQLPractice 
GO

-- Check if the table exists before creating it
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Tweets')
BEGIN
    CREATE TABLE Tweets (
        tweet_id INT,
        content VARCHAR(50)
    );
END;

-- Truncate the table
TRUNCATE TABLE Tweets;

-- Insert data into the table
INSERT INTO Tweets (tweet_id, content) 
VALUES (1, 'Vote for Biden');

INSERT INTO Tweets (tweet_id, content) 
VALUES (2, 'Let us make America great again!');

select * from Tweets
/*
Table: Tweets

+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| tweet_id       | int     |
| content        | varchar |
+----------------+---------+
tweet_id is the primary key (column with unique values) for this table.
This table contains all the tweets in a social media app.
 

Write a solution to find the IDs of the invalid tweets. The tweet is invalid if the number of characters used in the content of the tweet is strictly greater than 15.

Return the result table in any order.

The result format is in the following example.

 

Example 1:

Input: 
Tweets table:
+----------+----------------------------------+
| tweet_id | content                          |
+----------+----------------------------------+
| 1        | Vote for Biden                   |
| 2        | Let us make America great again! |
+----------+----------------------------------+
Output: 
+----------+
| tweet_id |
+----------+
| 2        |
+----------+
Explanation: 
Tweet 1 has length = 14. It is a valid tweet.
Tweet 2 has length = 32. It is an invalid tweet.
*/

select t.tweet_id from Tweets as t
where len(t.content) > 15