#Casey Nold; nold@pdx.edu; CS624 Final project
# how to run spark-submit --master yarn --num-executors ## eon_words.py
# This program finds the frequency that particular words occur in Tweets

from pyspark import SparkContext, SparkConf
import json
import re
from nltk.corpus import words, stopwords


def word_in_tweet(word, text):
    """
    check if a word exists in a tweet.
    Return true if so, else false
    """
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return (True,1)
    return (False,1)

# create spark context and open the files to search through
sc = SparkContext()
twitter_rdd = sc.textFile("hdfs://bigbird61.cslu.ohsu.edu:8020/data/archive_twitter/nov/11/07/*")

twitter_json = twitter_rdd.map(lambda j: json.loads(j))

text_tweets = twitter_json.filter(lambda x: x.get('text'))

twitter_comments = text_tweets.map(lambda c: c['text'])# this gives me a list of unicode texts

#search for words of interest
econ = twitter_comments.map(lambda tweet: word_in_tweet("economy",tweet)).reduceByKey(lambda a,b:a+b)
stock = twitter_comments.map(lambda tweet: word_in_tweet("stock market",tweet)).reduceByKey(lambda a,b:a+b)

# print
print("{'econ' 30:",econ.take(2),"}",'\n',"{'stock' 30:",stock.take(2),"}")
