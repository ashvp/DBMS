CREATE DATABASE twitter_data;

USE twitter_data;

CREATE TABLE tweets (
    tweet_id VARCHAR(50) PRIMARY KEY,
    content TEXT,
    likes INT,
    retweets INT,
    replies INT,
    quotes INT,
    author_id VARCHAR(50),
    query VARCHAR(255)
);

CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(255),
    followers_count INT,
    following_count INT,
    tweet_count INT
);

SELECT * FROM tweets;
SELECT * FROM users;