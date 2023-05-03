import tweepy
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ngrams
from nltk.stem import PorterStemmer
from collections import defaultdict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import warnings
from pylab import rcParams
from scipy.stats import f_oneway
from scipy.stats import ttest_ind
from textblob import TextBlob
from wordcloud import WordCloud
import re


consumer_key = 'bVJILv2OcmijEgLbnYh4x3GuG'
consumer_secret = 'T3IAvXHrjeHI7nL8mNDLlhulVpbmuBVuTkHeBsgQgHA21JyRQG'
access_token = '706715585648971776-FC8ZR5kwZIhvNTQDlAqNvJodxAV5vrm'
access_token_secret = 'TLT3OsjPN7ybQiVUPwFrf7WvikOtzltTJ32VKPmMylJSk'

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth, wait_on_rate_limit=True)

##############################
# Global variables
##############################

count_for_query = 100   # for search, maximum 100
pages_to_query = 1000
count_for_timeline_query = 50   # for query a user's timeline
language = 'en'
n_gram_size = 3
training_set_size = 10
most_informative_features_size = 15
top_n_words = 3000

avoid_words = ['https', 'News']
keywords = [' AI ', 'artificial intelligence', 'ChatGPT', 'machine learning']
keywords_variants = [' ai ', ' Ai ', 'chatgpt', 'chatGPT', 'Chatgpt']
keywords_all = keywords + keywords_variants

##############################
# Data collection from Twitter API
##############################

def query_by_keywords(key_word):
    all_tweets = []
    for query in key_word:
        query_and_operator = query + ' -filter:retweets'
        for page in tweepy.Cursor(api.search_tweets, q=query_and_operator, lang=language, count=count_for_query, tweet_mode='extended').pages(pages_to_query):
            for tweet in page:
                print("======")
                print("user: ", tweet.user.screen_name, tweet.user.id)
                print("created: ", tweet.created_at)
                print("Tweeted:", tweet.full_text)
                all_tweets.append(tweet)
    filtered_tweets = []
    for tweet in all_tweets: 
        if all([avoid_word not in tweet.full_text for avoid_word in avoid_words]):
            filtered_tweets.append(tweet)
    return filtered_tweets

def write_tweets_to_csv(tweets, filename):
    csvFile = open(filename, 'a')
    csvWriter = csv.writer(csvFile)
    for tweet in tweets:
        csvWriter.writerow([tweet.user.screen_name, tweet.full_text.encode('utf-8')])
    csvFile.close()

####### First Step. get users who has posted 1+ ai-related tweet ########

all_tweets = query_by_keywords(keywords_all)
print('total N of tweets of 1+ keywords', len(all_tweets))
write_tweets_to_csv(all_tweets, 'filtered tweets-all.csv')