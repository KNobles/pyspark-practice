import os
from dotenv import load_dotenv
import tweepy
from tweepy import StreamingClient, StreamRule

load_dotenv()

bearer_token = os.environ["BEARER_TOKEN"]

class TweetPrinterV2(StreamingClient):
    
    def on_tweet(self, tweet):
        print(f"{tweet.author_id}): {tweet.text}")
        print("-"*50)

printer = TweetPrinterV2(bearer_token=bearer_token)

# add new rules    
rule = StreamRule(value="giveaway")

# remove all rules
resp = printer.get_rules()
for data in resp.data:
    print(printer.delete_rules(ids=data.id))
# printer.filter()

printer.add_rules(rule)

printer.filter(expansions="author_id",tweet_fields="created_at")