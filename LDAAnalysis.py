# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 22:43:52 2014

@author: rishu
"""
import AnalyticsDB as ADB
import TweetDB as TDB
from EpiPipesApi import *
import lda
import numpy as np


for r in scan(TDB.session, distinct(TDB.session, proj(TDB.session, TDB.User_timeline, ['user_id']), ['user_id'])):
    user_id = r.user_id
    check_id = TDB.session.query(ADB.Usertimeline_category).filter(ADB.Usertimeline_category.user_id == user_id).all()
    if(len(check_id) != 0):
        print "user present", user_id
        continue
    
    print "processing user", user_id
    user_tweets= filterEQ(TDB.session, TDB.Tweet, 'user_id', user_id) #use only those tweets that are present in num_tweets
    
    user_words = distinct(TDB.session, proj(TDB.session, fuse(TDB.session, user_tweets, TDB.Words_in_tweet,  'id', 'tweet_id'), ['word_id']), ['word_id'])
    
    num_words = cardinality(TDB.session, user_words)
    num_tweets = cardinality(TDB.session, user_tweets)
    print "num_words ", num_words
    if(num_words < 50):
        continue
    col = 0
    word_to_col = {}
    vocab_list= []
    for w in scan(TDB.session, user_words):
        word_to_col[w.word_id] = col
        col = col + 1
        vocab_list.append(w.word_id)
    vocab = tuple(vocab_list)
    
    titles_list = []
    X = np.zeros((num_tweets, num_words))
    row = 0
    for t in scan(TDB.session, user_tweets):
        tweet_words = filterEQ(TDB.session, TDB.Words_in_tweet, 'tweet_id', t.id) 
        for tw in scan(TDB.session, tweet_words):
            col = word_to_col[tw.word_id]
            X[row, col] = X[row,col] +1
        titles_list.append(t.id)
        row=row+1
    
    titles=tuple(titles_list)     
    
    model = lda.LDA(n_topics=8, n_iter=500, random_state=1)
    model.fit(X)
    topic_word = model.topic_word_
    n_top_words = 8
    
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        for topic in topic_words:
            utc = ADB.Usertimeline_category(user_id=user_id, category_id=i, topic=topic)
            TDB.session.add(utc)
        #print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    
    doc_topic = model.doc_topic_
    for i in range(0, num_tweets):
        tweet_id = titles[i]
        category_id = doc_topic[i].argmax()
        if doc_topic[i][category_id] > 0: 
            tc  = ADB.Tweet_category(tweet_id = tweet_id, category_id = category_id)
            TDB.session.add(tc)
        else:
            print tweet_id, "has no category "
        #print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))
    TDB.session.commit()
    
