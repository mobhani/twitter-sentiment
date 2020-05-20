# libraries
import tweepy
import re

class twitterAPI:
    """
    This is a custom API used to scrape tweets using tweepy an regex
    """
    def __init__(self):
        try:
            # authenticates and connnects to twitter API
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_secret)
            self.api = tweepy.API(self.auth)
            print("Authentication successful!")

        except exception as e:
            print("Error in authentication.")
            print(e)


    def cleanTweets(self, tweets:dict):
        """
        This function is used to clean tweets of special characters, usernames,
        hyperlinks, and hashtags to process them
        """

        # converts dict values into list to iterate through
        values = list(tweets.values())

        # gets and stores locations of everything in lists to iterate through
        for tweet in range(len(values)):
            # copies raw tweet before cleaning
            clean_tweet = values[tweet]["text"]
            # stores tweet_id to add clean_tweet to tweets dict
            tweet_id = values[tweet]["id"]

            # gets index of urls and replaces with '#'
            for url in range(len(values[tweet]["entities"]["urls"])):
                start = int(values[tweet]["entities"]["urls"][url]['indices'][0])
                end = int(values[tweet]["entities"]["urls"][url]['indices'][1])
                diff = end - start
                clean_tweet = clean_tweet[:start] + '#' * diff + clean_tweet[end + 1:]

            # gets index of user_mentions and replaces with '#'
            for mention in range(len(values[tweet]["entities"]["user_mentions"])):
                start = int(values[tweet]["entities"]["user_mentions"][mention]['indices'][0])
                end = int(values[tweet]["entities"]["user_mentions"][mention]['indices'][1])
                diff = end - start
                clean_tweet = clean_tweet[:start] + '#' * diff + clean_tweet[end + 1:]

            # removes all '#' from tweet and adds into dict
            tweets[tweet_id]["clean_text"] = clean_tweet.replace('#', '').strip()

        return (tweets)


    def getTweetsByUser(self, username:str, _count:int, clean:bool = False):
        """
        This function is used to get tweets by username
        """

        # query using twitter API
        query = self.api.user_timeline(username)
        tweets = {}

        # iterates through query result and appends to list
        for tweet in query:
            tweets[tweet.id] = tweet._json

        # if clean paramater is set to True, helper function is called
        if clean:
            self.cleanTweets(tweets)

        return tweets


    def getUserDetails(self, username:str):
        """
        Test function to get user data
        """

        return self.api.get_user(username)
