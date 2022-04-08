import tweepy
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ngrams
from nltk.stem import PorterStemmer
from collections import defaultdict


consumer_key = "bVJILv2OcmijEgLbnYh4x3GuG"
consumer_secret = "T3IAvXHrjeHI7nL8mNDLlhulVpbmuBVuTkHeBsgQgHA21JyRQG"
access_token = "706715585648971776-FC8ZR5kwZIhvNTQDlAqNvJodxAV5vrm"
access_token_secret = "TLT3OsjPN7ybQiVUPwFrf7WvikOtzltTJ32VKPmMylJSk"

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
count_for_timeline_query = 50    # for query a user's timeline
language = "en"
n_gram_size = 3
training_set_size = 10
most_informative_features_size = 15
pages_to_query = 250
top_n_words = 3000


##############################
# Data collection from Twitter API
##############################

avoid_words = ["https", "News"]
drug_keywords = ["opioid", "codeine", "heroin", "demerol", "dilaudid", "percocet", "fentanyl"]
drug_keywords_variants = ["codine", "herion", "heroine", "demeral", "dilauded", "dilaudud", "dulaudid", "percs", "percocets", "percoset", "fentyl"]
drug_keywords_all = drug_keywords + drug_keywords_variants
# from paper "An Exploration of Social Circles and Prescription Drug Abuse Through Twitter"
abuse_keywords = ["too many", "too much", "overdose", "strong enough", "max", 'alcohol', 'happy pills', 'enough', 'not enough', 'rely', 'stressful', 'stress', 'inject', 'anxiety', 'anxious', 'dizz', 'faint', 'headache', 'shaky']
risk_keywords = abuse_keywords + drug_keywords

mental_distress_keywords = ["anxiety", "depression", "adhd", "insomnia", "psychiatric disorders", "borderline personality disorder", "ptsd disorders", "substance induced psychological disorders", "dissociative identity disorder", "multiple personality disorder", "panic disorder"]
legal_distress_keywords = ["legal", "problems", "issues", "criminal", "arrest", "prison", "incarcerations"]


def query_by_keywords(key_words_all):
    all_tweets = []
    for query in key_words_all[:1]:
        query_and_operator = query + " -filter:retweets"
        for page in tweepy.Cursor(api.search_tweets, q=query_and_operator, lang=language, count=count_for_query, tweet_mode='extended').pages(pages_to_query):
            for tweet in page:
                # print("======")
                # print("user: ", tweet.user.screen_name, tweet.user.id)
                # print("created: ", tweet.created_at)
                # print("Tweeted:", tweet.full_text)
                all_tweets.append(tweet)
    filtered_tweets = []
    for tweet in all_tweets: 
        if all([avoid_word not in tweet.full_text for avoid_word in avoid_words]):
            filtered_tweets.append(tweet)
    return filtered_tweets


def query_all_tweets_by_username(api, user_name):
    # return tweepy.Cursor(api.user_timeline, screen_name=user_name, count=count_for_timeline_query, tweet_mode="extended").items()
    return api.user_timeline(screen_name=user_name, count=count_for_timeline_query, tweet_mode='extended')


def filter_by_key_words(tweets, keywords):
    filtered_tweets = []
    for tweet in tweets:
        words = set(word_tokenize(tweet.full_text))
        if any([keyword in words for keyword in keywords]):
            filtered_tweets.append(tweet)
    return filtered_tweets


def get_users_abuse_related_history(api, users):
    filtered_tweets = []
    for user_name in users:
        all_tweets_from_user = query_all_tweets_by_username(api, user_name)
        filtered_tweets += filter_by_key_words(all_tweets_from_user, abuse_keywords)
        print("N of tweets on opioid || abuse till now", len(filtered_tweets))
    return filtered_tweets


def get_high_risk_users_and_tweets(api, users, keywords, threshold=1):
    risk_tweets = []
    for user in users:
        all_tweets_from_user = query_all_tweets_by_username(api, user)
        tweets_text_list = [tweet.full_text for tweet in all_tweets_from_user]
        count_risk_terms = 0
        risk_tweets_per_user = []
        for tweet in tweets_text_list:
            contain_keyword = False
            words = set(word_tokenize(tweet))
            for keyword in keywords:
                if keyword in words:
                    count_risk_terms += 1
                    contain_keyword = True
            if contain_keyword:
                risk_tweets_per_user.append((user, tweet))
        if count_risk_terms >= threshold:
            risk_tweets += risk_tweets_per_user
    return risk_tweets
        
def filter_tweets_by_keywords(filename, keywords, threshold=1):
    filtered_tweets = []
    tweets = open_file(filename)
    for user_name, tweet in tweets:
        words = set(word_tokenize(tweet))
        count_risk_terms = 0
        for keyword in keywords:
            if count_risk_terms >= threshold:
                break
            if keyword in words:
                count_risk_terms += 1
        filtered_tweets.append((user_name, tweets))
    with open("filter_tweets_by_keywords.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(filtered_tweets)
                

def write_tweets_to_csv(tweets, filename):
    csvFile = open(filename, 'a')
    csvWriter = csv.writer(csvFile)
    for tweet in tweets:
        csvWriter.writerow([tweet.user.screen_name, tweet.full_text.encode('utf-8')])
    csvFile.close()


def write_list_to_csv(users, filename):
    file = open(filename, 'a')
    for user in users:
        file.write(user + '\n')
    file.close()


def write_tuple_to_csv(items, filename):
    csvFile = open(filename, 'a')
    csvWriter = csv.writer(csvFile)
    for item in items:
        csvWriter.writerow([item[0], item[1].encode('utf-8')])
    csvFile.close()


def open_file(filename):
    # with open(filename) as file:
    #     listfile = []
    #     for line in file:
    #         listfile.append(line.strip())
    #     return listfile
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        return data


####### First Step. get users who has posted 1+ opioid-related tweet ########

# all_tweets = query_by_keywords(drug_keywords_all)
# print("total N of tweets of 1+ drug_key_words", len(all_tweets))
# all_users = set([tweet.user.screen_name for tweet in all_tweets])
# print("N users who has posted drug_key_words", len(all_users))
# write_tweets_to_csv(all_tweets, "all_tweets.csv")
# write_list_to_csv(all_users, "all_users.csv")

####### Next Step. get "high-risk" users ########

# all_users = open_file('all_users.csv')
# high_risk_users_and_tweets = []
# high_risk_users_and_tweets = get_high_risk_users_and_tweets(api, all_users[:50], threshold=3)
# print(len(high_risk_users_and_tweets))
# if high_risk_users_and_tweets:
#     write_tuple_to_csv(high_risk_users_and_tweets, "high_risk_users_and_tweets_1.csv")

# high_risk_users_and_tweets = get_high_risk_users_and_tweets(api, all_users[51:200], threshold=3)
# print(len(high_risk_users_and_tweets))
# if high_risk_users_and_tweets:
#     write_tuple_to_csv(high_risk_users_and_tweets, "high_risk_users_and_tweets_2.csv")

# Alternatively

filter_tweets_by_keywords("opioid_tweets.csv", abuse_keywords + legal_distress_keywords + mental_distress_keywords, threshold=2)


##############################
# Feature extraction
##############################

####### Next Step. add top N n-grams to featureset ########

# stop_words = set(stopwords.words("english"))
# sentence = "Let's test the n-grams implementation with this sample sentence! Yay!"
# ps = PorterStemmer()

def get_stemmed_word_list(sentence):
    words = word_tokenize(sentence)
    words = [w.lower() for w in words]
    # filter out stopwords
    filtered_words = [w for w in words if w not in stop_words]
    # stemming
    stemmed_words = [ps.stem(w) for w in filtered_words]
    print(stemmed_words)
    return stemmed_words


def generate_feature_matrix(word_features, word_list):
    feature_matrix = defaultdict(int)
    for word in word_list:
        if word in word_features:
            feature_matrix[word] += 1
    return feature_matrix


def get_all_words(tweets):
    all_words = []
    for tweet in tweets:
        stemmed_words = get_stemmed_word_list(tweet)
        all_words += ngrams(stemmed_words, n_gram_size)
    all_words = nltk.FreqDist(all_words)
    return all_words

# word_features = get_all_words(all_tweets)[:top_n_words]

####### Next Step. add enginerred word clusters to featureset  ########

# word_features += risk_keywords
# word_features += mental_distress_keywords
# word_features += legal_distress_keywords

# analyzer = SentimentIntensityAnalyzer()
# for sentence in sentences:
#     vs = analyzer.polarity_scores(sentence)
#     print("{:-<65} {}".format(sentence, str(vs)))


####### Next Step. generate feature matrix for each post  ########

# featuresets = [(generate_feature_matrix(word_features, word_list), category) for (word_list, category) in documents]


##############################
# Naive Bayes
##############################

def naive_bayes(featuresets):
    training_set = featuresets[:training_set_size]
    testing_set = featuresets[training_set_size:]
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print("NB accuracy: ", nltk.classify.accuracy(classifier, testing_set))
    classifier.show_most_informative_features(most_informative_features_size)