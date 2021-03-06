# -*- coding: utf-8 -*-
"""positivetweets.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10AA3w0XT6AcB8cfJdOc1nKrpW9fCrefM
"""

# # !pip install tweepy
# !pip install textblob

from textblob import TextBlob, Word, Blobber
from textblob.classifiers import NaiveBayesClassifier
from textblob.taggers import NLTKTagger

import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob

class TwitterClient(object): 
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
		''' 
		Class constructor or initialization method. 
		'''

    
		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
		''' 
		Utility function to classify sentiment of passed tweet 
		using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 10): 
		''' 
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = [] 

		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count) 
			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 
        
        # saving text of tweet 
				parsed_tweet['text'] = tweet.text
        
        # saving sentiment of tweet 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e))

def main(): 
	# creating object of TwitterClient Class 
  api = TwitterClient() 
#   name = ['Donald Trump', 'Joe Biden', "Beto O'Rourke", 'Amy Klobuchar', 'Kamala Harris', 'Cory Booker']
  name = ['@realDonaldTrump', '@JoeBiden', '@ewarren', '@BetoORourke', '@amyklobuchar','@KamalaHarris', '@PeteButtigieg', '@CoryBooker']
  
  for i in name:
      # calling function to get tweets 
      tweets = api.get_tweets(query = i, count = 1500) 
      print("\n")
      print(i) 
      # {0:.0f}%".format(1/3 * 100)

      # picking positive tweets from tweets 
      ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
      # percentage of positive tweets 
      print("Positive tweets percentage: {0:.1f} %".format(100*len(ptweets)/len(tweets))) 
      print (f"Number positive tweets:  {len(ptweets)}")
      # picking negative tweets from tweets 
      ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 

      # percentage of negative tweets 
      print("Negative tweets percentage: {0:.1f} %".format(100*len(ntweets)/len(tweets))) 
      print (f"Number negative tweets:  {len(ntweets)}")

      # percentage of neutral tweets 
      print("Neutral tweets percentage: {0:.1f} %".format(100*(len(tweets) - (len(ntweets + ptweets)))/len(tweets))) 
      print (f"Number Neutral tweets:  {len(tweets) - (len(ntweets + ptweets))}")
      #     # printing first 5 positive tweets 
      #     print("\n\nPositive tweets:") 
      #     for tweet in ptweets[:10]: 
      #       print(tweet['text']) 

      #     # printing first 5 negative tweets 
      #     print("\n\nNegative tweets:") 
      #     for tweet in ntweets[:10]: 
      #       print(tweet['text'])

if __name__ == "__main__": 
	# calling main function 
	
  
  main()



















