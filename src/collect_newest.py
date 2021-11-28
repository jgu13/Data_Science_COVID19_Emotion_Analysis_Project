import tweepy
import pandas as pd

ACCESS_TOKEN = "hkOQnAi7dkDuMV6bYfMcOiPlP"
ACCESS_SECRET = "xJEGVdTqFIrxLDS4SDQCiLQ8lEFxeMlr8ngWiEKvT8hoxmQDd1"
CONSUMER_KEY = "1463555178968150020-565j9P2FrNaO5DIg1zIkIAHMBzleFD"
CONSUMER_SECRET = "eU8qW2jICXN3ja7AUtd0Ow5ObCY4GG4mTR8yNoaCqSItT"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIKXWAEAAAAAeNdxPfsCLIjYQ%2BWq%2F8aNiXxGHxU%3Dib30FiO9uUN9t6cDDR79wDCRh3yctmiFafP9Y7NHLCB3lbGFBY"

# authenticate
# client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
#                        access_token=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET, wait_on_rate_limit=True)

client = tweepy.Client(bearer_token=BEARER_TOKEN)

# for city, lg in places_lgs.items():
#     # return up to 20 places in each city
#     places = api.reverse_geocode(lat=lg[0], log=lg[1], accuracy="600ft", granularity="city")

query = "covid OR covid-19 OR vaccination OR vaccine OR Pfizer OR Moderna OR 'Johnson&Johnson vaccine'"
tweets = []
responses = tweepy.Paginator(client.search_recent_tweets, query, expansions=['geo.place_id'], place_fields=['country_code'],
                             start_time='2021-11-24T00:00:00Z', tweet_fields=['text'], user_fields=['location']).flatten()
for response in responses:
    print(response.json())
    tweets.append(response)
print("Total tweets collected: ", len(tweets))

# tweet_df = pd.DataFrame()
# for tweet in tweets:
#     tweet_df.append({'country': tweet
#                      'text': tweet.text})
#
# print(tweet_df.head())

# class Stream(tweepy.Stream):
#     def on_status(self, status):
#         if status.retweet:
#             return
#         location = status.user.location
#         text = status.text
#
# class ConnectionTester(tweepy.Stream):
#     def on_connection_error(self):
#         self.disconnect()
#
# # initialize a stream
# stream = tweepy.Stream(
#   TWITTER_APP_KEY, TWITTER_APP_SECRET,
#   TWITTER_KEY, TWITTER_SECRET
# )
#
# # connect and run a stream
# keywords = ["COVID", "COVID-19", "vaccination", "vaccinations", "Pfizer", "Moderna", "Johnson&Johnson vaccine"]
# stream.filter(track=keywords, languages=['en'])




