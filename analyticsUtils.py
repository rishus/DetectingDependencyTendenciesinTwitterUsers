# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 11:45:48 2014

@author: rishu
"""

from EpiPipesApi import *
import TweetDB as TDB



def TweethasShopping(tweet_id):
    res = scan(TDB.session, filterEQ(TDB.session, TDB.Tweet, 'id', tweet_id))
    if(len(res) == 0):
        print "No tweet found "
        return 0
    
    tweet_words = filterEQ(TDB.session, TDB.Words_in_tweet, 'tweet_id', tweet_id)
    shopping_words = fuse(TDB.session, tweet_words, TDB.Shopping_keywords, 'word_id', 'm_word_id')
    num_shopping_words = cardinality(TDB.session, shopping_words)
    return num_shopping_words
    
    


money = re.compile('|'.join([
  r'^\$?(\d*\.\d{1,2})$',  # e.g., $.50, .50, $1.50, $.5, .5
  r'^\$?(\d+)$',           # e.g., $500, $5, 500, 5
  r'^\$(\d+\.?)$',         # e.g., $5.
]))

def TweethasAmount(tweet_id):
    res = scan(TDB.session, filterEQ(TDB.session, TDB.Tweet, 'id', tweet_id))
    if(len(res) == 0):
        print "No tweet found "
        return 0
    all_match = []
    tweet_words = filterEQ(TDB.session, TDB.Words_in_tweet, 'tweet_id', tweet_id)
    res = scan(TDB.session, tweet_words)
    for r in res:
        result = money.atch(r.word_id)
        if result is not None:
            all_match.append(result)
    print all_match
    return all_match