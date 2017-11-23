
#import json, sys
from collections import defaultdict
from spam_detector_commons import *
import os
import TweetDB as TDB
from EpiPipesApi import *
from nltk.corpus import words
import nltk

D = set()
wordProb = {'B':defaultdict(int), 'G': defaultdict(int)}
wordSize = {'B': 0, 'G': 0}
docCount = {'B': 0, 'G': 0}

def feedModel(spamTrainingData):
    global docCount, D, wordProb, wordSize

    for tweet in spamTrainingData:
        klass = tweet.cl 
        if klass == 'B':
            attr =  tweet.text     
            docCount[klass] += 1
            
            for w in getFeatures(attr):
                D.add(w)
                wordProb[klass][w] += 1
                wordSize[klass] += 1

    ctr = 0
    for tweet in spamTrainingData:
        if ctr == 4005:
            break
        klass = tweet.cl 
        
        if klass == 'G':
            attr =  tweet.text     
            docCount[klass] += 1
            ctr += 1
            for w in getFeatures(attr):
                D.add(w)
                wordProb[klass][w] += 1
                wordSize[klass] += 1
                
#    klass = 'G'
#    for word in words.words():
#        docCount[klass] += 1
#        for w in getFeatures(word):
#            D.add(w)
#            wordProb[klass][w] += 1
#            wordSize[klass] += 1
    
#    all_novels = nltk.corpus.gutenberg.fileids()
#    for nov in all_novels[0:2]:
#        emma = nltk.corpus.gutenberg.words(nov)
#        docCount[klass] += 1
#        D.add(nov)
#        for word in emma:
#            word = str(word)
#            #docCount[klass] += 1
#            for w in getFeatures(word):
#                #D.add(w)
#                wordProb[klass][w] += 1
#                wordSize[klass] += 1


modelFileName = 'spam_filter_model.txt'

if os.path.isfile(modelFileName):
    #(docCount, wordSize, wordProb,  D) = readModel(modelFileName)
    print "HELLO"
else:
    D = set()
    wordProb = {'B':defaultdict(int), 'G': defaultdict(int)}
    wordSize = {'B': 0, 'G': 0}
    docCount = {'B': 0, 'G': 0}


spamTrainingData = scan(TDB.session, TDB.Spamtweet_training_tweet)

feedModel(spamTrainingData)

#writeModel(modelFileName, docCount, wordSize, wordProb, D)




#for tweet in spamTrainingData:
#    klass = 'B' #spammer.cl  #parts[0]
#    attr =  tweet.text     #json.loads(parts[1])
#    tweet_id = tweet.tweet_id
#    user_id = tweet.user_id
#    docCount[klass] += 1
#
#    for w in getFeatures(attr):
#        D.add(w)
#        wordProb[klass][w] += 1
#        wordSize[klass] += 1
#        
#writeModel(modelFileName, docCount, wordSize, wordProb, D)
#

#
#(docCount, wordSize, wordProb, D) = readModel(modelFileName)
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

