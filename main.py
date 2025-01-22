import praw
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import pickle
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.stream import TradingStream
import config

reddit = praw.Reddit(
    client_id=config.REDDIT_CLIENT_ID,
    client_secret=config.REDDIT_CLIENT_SECRET,
    user_agent=config.REDDIT_USER_AGENT,
    username=config.REDDIT_USERNAME,
    password=config.REDDIT_PASSWORD
)

client = TradingClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY, paper=True)

def getStockSentiments(posts, tickers):
    sid = SentimentIntensityAnalyzer()

    ticker_dict = {ticker: [] for ticker in tickers}

    tickers_delimited = "|".join(ticker for ticker in tickers)
    pattern = fr'\b({tickers_delimited})\b'

    print('Finding posts with stock tickers:')

    for post in posts:
        text = post.title
        matches = set(re.findall(pattern, text))

        if (matches):
            sentiment_score = sid.polarity_scores(text)['compound']
            print(f'{text:<150}{",".join(match for match in matches):>20}{sentiment_score:>10}')
            for match in matches:
                ticker_dict[match].append(sentiment_score)

    return ticker_dict

def getHighestAvgSentiment(sentiments):
    highest_avg_key = None
    highest_avg_value = float('-inf')

    for key, value in sentiments.items():
        if (value):
            avg_sentiment = sum(value) / len(value)
            if avg_sentiment > highest_avg_value:
                highest_avg_value = avg_sentiment
                highest_avg_key = key

    return highest_avg_key

if __name__ == "__main__":
    with open('tickers.pkl', 'rb') as f:
        tickers = pickle.load(f)

    subreddit = reddit.subreddit('wallstreetbets')
    top_posts = subreddit.top(time_filter = 'all', limit=None)

    sentiments = getStockSentiments(top_posts, tickers)

    stockToBuy = getHighestAvgSentiment(sentiments)

    print(f'Submitting Buy Order for: {stockToBuy}')

    order_details = MarketOrderRequest(
        symbol = stockToBuy,
        notional = 1000,
        side = OrderSide.BUY,
        time_in_force = TimeInForce.DAY
    )

    # order = client.submit_order(order_data = order_details)
    