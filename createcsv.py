import praw
import config
import csv

reddit = praw.Reddit(
    client_id=config.REDDIT_CLIENT_ID,
    client_secret=config.REDDIT_CLIENT_SECRET,
    user_agent=config.REDDIT_USER_AGENT,
    username=config.REDDIT_USERNAME,
    password=config.REDDIT_PASSWORD
)

posts = set()

subreddit = reddit.subreddit('wallstreetbets')
all_posts = subreddit.top(time_filter = 'all', limit=None)
month_posts = subreddit.top(time_filter = 'year', limit=None)
posts.update(all_posts)
posts.update(month_posts)

with open("postsWithSentiment.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    writer.writerow(["Title", "Sentiment"])
    
    for post in posts:
        writer.writerow([post.title, 0])

# From here, manually change the sentiment of each post to 1, 0, or -1 to create training data