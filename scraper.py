import praw
import config
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import csv
import re

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()
 
tickers = list()
with open('tickers.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        ticker = row[0].split(',')[0].strip('"')
        tickers.append(ticker)

print(tickers)

pattern = r'\b\$?(' + '|'.join(re.escape(ticker) for ticker in ticker) + r')\b'

reddit = praw.Reddit(
    client_id=config.REDDIT_CLIENT_ID,
    client_secret=config.REDDIT_CLIENT_SECRET,
    user_agent=config.REDDIT_USER_AGENT,
    username=config.REDDIT_USERNAME,
    password=config.REDDIT_PASSWORD
)

def fetch_top_posts(subreddit_name):
    # ticker_sentiments = dict(list)

    subreddit = reddit.subreddit(subreddit_name)
    top_posts = []
    seen_posts = set()
    for timeframe in ['day']:
        for post in subreddit.top(time_filter = timeframe, limit=None):
            if post.id not in seen_posts:
                top_posts.append({
                    'title': post.title,
                    'selftext': post.selftext,
                    # 'score': post.score,
                    # 'created_utc': post.created_utc,
                    # 'url': post.url
                })
                seen_posts.add(post.id)
                text = f"{post.title}"
                sentiment_score = sid.polarity_scores(text)
                matches = re.findall(pattern, text)
                print(text)
                print(matches)
                print(f"Score: {sentiment_score}")
    return top_posts

if __name__ == "__main__":
    print("main")
    # posts = fetch_top_posts('wallstreetbets')
    # print(f"Fetched {len(posts)} posts")
    