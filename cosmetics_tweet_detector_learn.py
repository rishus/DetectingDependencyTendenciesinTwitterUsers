# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 14:47:11 2014

@author: rishu
"""


#import json, sys
from collections import defaultdict
from spam_detector_commons import *
import os
import TweetDB as TDB
from EpiPipesApi import *
modelFileName = 'beauty_filter_model.txt'

if os.path.isfile(modelCosmeticTweetFileName):
    (docCount, wordSize, wordProb, D) = readModel(modelFileName)
else:
    D = set()
    wordProb = {'Y':defaultdict(int), 'N': defaultdict(int)}
    wordSize = {'Y': 0, 'N': 0}
    docCount = {'Y': 0, 'N': 0}

#(docCount, wordSize, wordProb, D) = readModel(modelFileName)
#
cosmeticsTrainingData = scan(TDB.session, TDB.cosmetics_tweet)
for tweet in spamTrainingData:
    klass = 'Y' #spammer.cl  #parts[0]
    attr =  tweet.text     #json.loads(parts[1])
    tweet_id = tweet.tweet_id
    user_id = user.user_id
    docCount[klass] += 1

    for w in getFeatures(attr):
        D.add(w)
        wordProb[klass][w] += 1
        wordSize[klass] += 1
        
writeModel(modelFileName, docCount, wordSize, wordProb, D)




#def main():
#    modelFileName = sys.argv[1]
#    D = set()
#    wordProb = {'B':defaultdict(int), 'G': defaultdict(int)}
#    wordSize = {'B': 0, 'G': 0}
#    docCount = {'B': 0, 'G': 0}
#
#    for line in sys.stdin.readlines():
#        parts = line.strip().split("\t")
#        klass = parts[0]
#        attr = json.loads(parts[1])
#        docCount[klass] += 1
#
#        for w in getFeatures(attr):
#            D.add(w)
#            wordProb[klass][w] += 1
#            wordSize[klass] += 1
#            
#    writeModel(modelFileName, docCount, wordSize, wordProb, D)
#
#main()

