# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 17:31:33 2014

@author: rishu
"""
from spam_detector_commons import *
from EpiPipesApi import *
import TweetDB as TDB 
import re

#model = readModel('spam_filter_model.txt')
model = (docCount, wordSize, wordProb, D)
spamTrainingData = scan(TDB.session, TDB.Spamtweet_training_tweet)
num_correct = 0

for tweet in spamTrainingData:
    text = tweet.text
    #text = re.sub('[@]', '', text)
    pc = classify(model, text)
    if(tweet.cl != pc):
        print  num_correct, tweet.text, tweet.cl, pc
    else:
        num_correct  += 1
    if num_correct%100 == 0 :
        print num_correct