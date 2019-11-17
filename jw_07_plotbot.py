import numpy as np
import pandas as pd
import matplotlib
# AGG backend used for writing to file
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import tweepy
import time

from myconfig import consumer_key, consumer_secret, access_token, access_token_secret
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Setup tweepy and vader
analyzer = SentimentIntensityAnalyzer()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

def AnalyzeTweets():
    plotbot_tweets = api.search(q="@projecttestonly Analyze:")
    target_account = ""
    
    # Most recent
    last_tweet = plotbot_tweets["statuses"][0]["text"]
    username = plotbot_tweets["statuses"][0]["user"]["screen_name"]
    
    # What is plotbot asking to analyze
    try: 
        splits = last_tweet.split("Analyze:")
        target_account = splits[1].strip()
        print(f"Target account: {target_account}")
    except Exception:
        raise
    
    # To check if plotbot had already asked for this, look at the user_timeline
    all_plotbot_tweets = api.user_timeline()
    
    # For accounts with no tweets, make the first tweet to ensure user_timeline() is not empty
    if all_plotbot_tweets == list():
        api.update_status("Excited to start tweeting!")
        all_plotbot_tweets = api.user_timeline()
        
    # Required that account has a minimum of one tweet
    for tweet in all_plotbot_tweets:
        # Check if repeat
        if target_account in tweet["text"]:
            print("Repeated request.")
            # If repeat, stop here
            return
        else:
            print("Request in progress...")
            # make sure to keep outside for loop
            tweet_data = {
                "tweet_source": [],
                "tweet_text": [],
                "tweet_date": [],
                "tweet_vader_score": [],
                "tweet_neg_score": [],
                "tweet_pos_score": [],
                "tweet_neu_score": []
            }
            # Paginate for 500 tweets
            for x in range(25):
                public_tweets = api.user_timeline(target_account, page=x)
                for tweet in public_tweets:
                    tweet_data["tweet_source"].append(tweet["user"]["name"])
                    tweet_data["tweet_text"].append(tweet["text"])
                    tweet_data["tweet_date"].append(tweet["created_at"])

                    results = analyzer.polarity_scores(tweet["text"])
                    tweet_data["tweet_vader_score"].append(results["compound"])
                    tweet_data["tweet_pos_score"].append(results["pos"])
                    tweet_data["tweet_neu_score"].append(results["neu"])
                    tweet_data["tweet_neg_score"].append(results["neg"])
            tweet_df = pd.DataFrame.from_dict(tweet_data)
            # Convert to datetime objects then sort
            tweet_df["tweet_date"] = pd.to_datetime(tweet_df["tweet_date"])
            tweet_df.sort_values("tweet_date", inplace=True)
            tweet_df.reset_index(drop=True, inplace=True)
            
            # Clear plot
            plt.clf()
            plt.plot(np.arange(-len(tweet_df["tweet_vader_score"]), 0, 1),
                         tweet_df["tweet_vader_score"], marker="o", linewidth=0.5,
                         alpha=0.8, label=f"{target_account}")
            plt.title(f"Sentiment Analysis of Tweets ({time.strftime('%x')}")
            plt.ylabel("Tweet Polarity")
            plt.xlabel("Tweets Ago")
            plt.xlim([-len(tweet_df["tweet_vader_score"]) - 7, 7])
            plt.ylim([-1.05, 1.05])
            plt.grid()

            lgnd = plt.legend(fontsize="small", mode="Expanded",
                                      loc="best", bbox_to_anchor=(1, 1), title="Tweets", labelspacing=0.5)
            file_path = "analysis/" + target_account + ".png"
            plt.savefig(file_path, bbox_extra_artists=(lgnd, ), bbox_inches='tight')
            print(f"Plot complete for {target_account}!")
            api.update_with_media(file_path, f"New Tweet Analysis: {target_account} (Thx @{username}!)")
            print(f"Updated status for {target_account}!")

while(True):
    AnalyzeTweets()
    time.sleep(300)