# Casey Nold; nold@pdx.edu; Final Project CS624
# how to run spark-submit --master yarn --num-executors ## pos_neg.py
# This program is used to extract the frequency that positive and negative
# words occur in tweets 

from pyspark import SparkContext, SparkConf
import json
import re
from nltk.corpus import words, stopwords

file1 = "positive_words.txt"
file2 = "negative_words.txt"

def reader(filename):
    """
    Read a data file in, and return the values
    """
    with open(filename,'r') as f:
        data = f.readlines()
    return data

def list_maker(data):
    """
    Make a list from read-in file lines. Return a list
    """
    words = []
    for i in range(35,len(data)):
        words.append(data[i].rstrip('\n'))
    return words

def word_in_tweet(text, word):
    """
    Check to see if a particular word is in a tweet.
    """
    if word in text:
        return (True,1)
    return (False,1)

# obtain the word lists
pos_data = reader(file1)
neg_data = reader(file2)

# convert to lists
pos_list = list_maker(pos_data)
neg_list = list_maker(neg_data)


sc = SparkContext()
twitter_rdd = sc.textFile("hdfs://bigbird61.cslu.ohsu.edu:8020/data/archive_twitter/nov/11/30/*")

twitter_json = twitter_rdd.map(lambda j: json.loads(j))

text_tweets = twitter_json.filter(lambda x: x.get('text'))

twitter_comments = text_tweets.map(lambda c: c['text'])# this gives me a list of unicode texts

tweet_wl = twitter_comments.flatMap(lambda x: x.strip("#").strip().lower().split())

# Find the positive and negative words according to the positive and negative lists
pos = tweet_wl.map(lambda tweet: word_in_tweet(set(pos_list),tweet)).reduceByKey(lambda a,b:a+b)
neg  = tweet_wl.map(lambda tweet: word_in_tweet(set(neg_list),tweet)).reduceByKey(lambda a,b:a+b)

# print
print("{'positive' :",pos.take(2),"}","{'negative' :", neg.take(2))
