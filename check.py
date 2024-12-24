import tweepy
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

# Twitter API credentials


# MySQL connection details
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Snucse@123',
    'database': 'twitter_data'
}

# Initialize the Twitter client
client = tweepy.Client(bearer_token=os.environ.get("BEARER_TOKEN"))

# Connect to MySQL database
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Function to fetch and store tweets and users
def fetch_and_store_tweets(query):
    response = client.search_recent_tweets(
        query=query,
        max_results=10,
        tweet_fields=['public_metrics', 'author_id'],
        expansions=['author_id'],
        user_fields=['public_metrics']
    )

    # Insert tweets into the tweets table
    for tweet in response.data:
        metrics = tweet.public_metrics
        tweet_query = """
        INSERT INTO tweets (tweet_id, content, likes, retweets, replies, quotes, author_id, query)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            likes = VALUES(likes),
            retweets = VALUES(retweets),
            replies = VALUES(replies),
            quotes = VALUES(quotes);
        """
        cursor.execute(tweet_query, (
            tweet.id, tweet.text, metrics['like_count'], metrics['retweet_count'],
            metrics['reply_count'], metrics['quote_count'], tweet.author_id, query
        ))

    # Insert users into the users table
    users = {user.id: user for user in response.includes['users']}
    for user_id, user in users.items():
        metrics = user.public_metrics
        user_query = """
        INSERT INTO users (user_id, username, followers_count, following_count, tweet_count)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            followers_count = VALUES(followers_count),
            following_count = VALUES(following_count),
            tweet_count = VALUES(tweet_count);
        """
        cursor.execute(user_query, (
            user.id, user.username, metrics['followers_count'],
            metrics['following_count'], metrics['tweet_count']
        ))

    # Commit the changes
    conn.commit()

# Example usage
try:
    fetch_and_store_tweets("python programming")
    print("Data successfully fetched and stored in MySQL.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cursor.close()
    conn.close()
