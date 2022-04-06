import tweepy
import csv #Import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ngrams
from nltk.stem import PorterStemmer


consumer_key = "bVJILv2OcmijEgLbnYh4x3GuG"
consumer_secret = "T3IAvXHrjeHI7nL8mNDLlhulVpbmuBVuTkHeBsgQgHA21JyRQG"
access_token = "706715585648971776-FC8ZR5kwZIhvNTQDlAqNvJodxAV5vrm"
access_token_secret = "TLT3OsjPN7ybQiVUPwFrf7WvikOtzltTJ32VKPmMylJSk"

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth)

count_for_query = 100   # maximum
language = "en"

##############################
# Data collection from Twitter API
##############################

# key_words = ["opioid", "codeine", "heroin", "demerol", "dilaudid", "percocet", "fentanyl"]
# key_words_variants = ["codine", "herion", "heroine", "demeral", "dilauded", "dilaudud", "dulaudid", "percs", "percocets", "percoset", "fentyl"]
# key_words_all = key_words + key_words_variants
# all_tweets = []
# for query in key_words_all[:1]:
#     query_and_operator = query + " -filter:retweets"
#     for page in tweepy.Cursor(api.search_tweets, q=query_and_operator, lang=language, count=count_for_query, tweet_mode='extended').pages(10):
#         for tweet in page:
#             # print("======")
#             # print("user: ", tweet.user.screen_name, tweet.user.id)
#             # print("Tweeted:", tweet.text)
#             all_tweets.append(tweet)

# avoid_words = ["https", "News"]
# filtered_tweets = []
# for tweet in all_tweets: 
#     if all([avoid_word not in tweet.full_text for avoid_word in avoid_words]):
#         filtered_tweets.append(tweet)

# csvFile = open('result.csv', 'a')
# csvWriter = csv.writer(csvFile)
# for tweet in filtered_tweets:
#     csvWriter.writerow([tweet.created_at, tweet.user.screen_name, tweet.full_text.encode('utf-8')])
# csvFile.close()


# def extract_all_tweets_by_username(api, name):
#     all_tweets = []
#     while True:
#         tweets = api.user_timeline(id=name, count=tweetCount, tweet_mode = 'extended')
#         for tweet in tweets:
#             print("=======")
#             print(tweet.full_text)
#         if len(tweets) == 0:
#             break
#         all_tweets.extend(tweets)
#         print('N of tweets downloaded till now {}'.format(len(all_tweets)))

# extract_all_tweets_by_username(api, "nytimes")


##############################
# Feature extraction
##############################

stop_words = set(stopwords.words("english"))
n = 3
sentence = "Let's test the n-grams implementation with this sample sentence! Yay!"
ps = PorterStemmer()

def get_n_grams(sentence, n):
    words = word_tokenize(sentence)
    # filter out stopwords
    filtered_words = [w for w in words if w not in stop_words]
    print(filtered_words)
    # stemming
    stemmed_words = [ps.stem(w) for w in filtered_words]
    print(stemmed_words)
    # n-gram
    n_grams = ngrams(stemmed_words, n)
    for grams in n_grams:
        print(grams)

# get_n_grams(sentence, n)

