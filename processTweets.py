# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 15:37:33 2014

@author: rishu
"""

import re
import TweetDB as TDB
from EpiPipesApi import *
#from microsofttranslator import Translator
from processTweet import *
from collections import Counter
import time

sentenceEnders = re.compile('[,.!?:;]')
regexp = re.compile("(?P<url>https?://[^\s]+)")
urldelims = ["!", "*", "'", "(", ")", ";", ":", "@" , "&", "=", "+", "$", ",", "/", "?","%", "#", "[", "]"]
#translator = Translator('DAproject14', 'dCFsqRcD33p56jvHk12pO/PQy//h/+WnhTwuwtLfl6k=')
#print translator.translate("Hello", "pt")

hashtags = []
contacts = []
urls = []
dropped = []
finalWordList = []
start = time.time()
uoi = scan(TDB.session, TDB.User_timeline)
session_ctr = 1
for u in uoi:
    
    check_id = TDB.session.query(TDB.Words_in_tweet).filter(TDB.Words_in_tweet.tweet_id==u.tweet_id).all()
    if (len(check_id)==0):
        t = scan(TDB.session, filterEQ(TDB.session, TDB.Tweet, 'id', u.tweet_id))
        #start1 = time.time()
        [hts, ct, ur, wl, dp] = processTweet(t[0].text, regexp, urldelims, sentenceEnders)
        #print "PTime ", time.time() - start1
#        hhts = []
#        for h in hts:
#            hhts.append('#' + h)
        finalWordList = wl + hts
        for word in finalWordList:
        #if (len(check_id) == 0):
            wid = TDB.Words_in_tweet(tweet_id = t[0].id, word_id = word)
            TDB.session.add(wid)
    if(session_ctr%1000 == 0):
        TDB.session.commit()
        print "Time ", time.time() - start
        start = time.time()
    session_ctr += 1
    
#
#tweet_keywords = fuse(TDB.session, TDB.Words_in_tweet, TDB.Keywords, 'word_id', 'ketword')
#tweet_keywords_count = aggregate(TDB.session, )
#kws = scan(TDB.session, TDB.Keywords)
#for kw in kws:
    

#tweets = scan(TDB.session, TDB.Tweet)
#print len(tweets)
#count = 0
#ctr = 0
#for tweet in tweets:
#    #start = time.time()
#    [hts, ct, ur, wl, dp] = processTweet(tweet.text, regexp, urldelims, sentenceEnders)
#    #hashtags += hts
#    #contacts += ct
#    #urls += ur
#    #dropped += dp
##    finalWordList += wl
#    finalWordList = wl + hts
#    for word in set(wl):
##        check_id = TDB.session.query(TDB.Words_in_tweet).filter(TDB.Words_in_tweet.tweet_id==tweet.id).filter(TDB.Words_in_tweet.word_id==word).all()
#        #if (len(check_id) == 0):
#        wid = TDB.Words_in_tweet(tweet_id = tweet.id, word_id = word)
#        TDB.session.add(wid)
#    ctr = ctr+1
#    if ctr==1000:
#        TDB.session.commit()
#        ctr=0
#TDB.session.commit()


    #print "Time taken ", time.time() - start
    # hashtag tables
#    if len(hts) > 0:
#        for ht in hts:
#            check_id = TDB.session.query(TDB.Hashtag_in_tweet).filter(TDB.Hashtag_in_tweet.tweet_id == 
#            tweet.id).filter(TDB.Hashtag_in_tweet.hash_id == ht)
#            if len(check_id) == 0:
#                ht = TDB. Hashtag_in_tweet(hash_id = ht, tweet_id = tweet.id, topic='cosmetics')
#                TDB.session.add(ht)
#                print ht
#            else:
#                print ht , 'already present'
#            
#            check_id = TDB.session.query(TDB.Hashtag).filter(TDB.Hashtag == ht)
#            if len(check_id) == 0:
#                ht = TDB. Hashtag(hash)
                
    
 
#cnt = Counter()
#for ht in hashtags:
#    cnt[ht] += 1
#    
#mcht = cnt.most_common()
#
#
#cnt = Counter()
#for word in finalWordList:
#    cnt[word] += 1
#    
#mcw = cnt.most_common()

#users = scan(TDB.session, TDB.Tweet)
#cnt = Counter()
#for word in finalWordList:
#    cnt[name] += 1
#    
#mcn = cnt.most_common()



#""" build adjacency matrix """

#A = np.zeros((numKeywords, numUsers))
#usrWts = np.ones((numKeywords, 1))
#for i in range(0, numKeywords):
#    for j in range(0, numUsers):

