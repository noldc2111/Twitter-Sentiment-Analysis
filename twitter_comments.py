# Casey Nold; nold@pdx.edu; Final Project CS624
# how to run spark-submit --master yarn --num-executors ## twitter_comments.py
# This code uses the python API for spark to get the word frequency from tweets

from pyspark import SparkContext, SparkConf
import datetime as dt
import json
from nltk.corpus import words, stopwords

# aquire the a list of words and stop words
word_list =  words.words()
stp_wl    = stopwords.words("english")

lowered_wl = []

# normalize the word list to be all lowered
for each in word_list:
    lowered_wl.append(each.lower())


sc = SparkContext()
twitter_rdd = sc.textFile("hdfs://bigbird61.cslu.ohsu.edu:8020/data/archive_twitter/nov/11/01/*")
twitter_json = twitter_rdd.map(lambda x: json.loads(x))

# By using the dict.get(key)-- I avoid key error which occurs b/c 'text' may not be present
text_tweets = twitter_json.filter(lambda x: x.get('text'))

twitter_comments = text_tweets.map(lambda c: c['text'])# this gives me a list of unicode texts

# This line splits the text up into single words.
# the strip('#') doesn't work for some reason....
tweet_wl = twitter_comments.flatMap(lambda x: x.strip("#").strip().lower().split()) 

# then the next step would be to filter the words by some english dictionary
# also to filter out the hashtags!

# obtain all the english words
english_words = tweet_wl.filter(lambda s: s in lowered_wl)

# english words sans stop words
rm_sw_english = english_words.filter(lambda st: st not in stp_wl) 

# map reduce to find the frequency
freq = rm_sw_english.map(lambda x: (x,1)).reduceByKey(lambda a,b: a+b)

# save the RDD
freq.saveAsTextFile("twitter_wordfreq_total.txt")

