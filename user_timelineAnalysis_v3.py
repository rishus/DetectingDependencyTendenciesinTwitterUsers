from datetime import datetime
import datetime
from dateutil import parser
from EpiPipesApi import *
import TweetDB as TDB
import numpy as np
import lda
#for each timeline
#order tweets by date

beauty_keywords = set()
shopping_keywords=set()
for kw in scan(TDB.session, TDB.Keywords):
    beauty_keywords.add(kw.keyword)

for kw in scan(TDB.session, TDB.Shopping_keywords):
    shopping_keywords.add(kw.m_word_id)

def get_regret_tweets(uid):
    rt = set()
    for row in TDB.engine.execute('select * from regret_tweets where user_id = ' + str(uid)):
        rt.add(row.id)
    return rt

def get_sorrynosorry_tweets(uid):
    rt = set()
    for row in TDB.engine.execute('select * from sorrynosorry where user_id = ' + str(uid)):
        rt.add(row.id)
    return rt

def get_money_tweets(uid):
    rt = set()
    for row in TDB.engine.execute('select * from money_tweets where user_id = ' + str(uid)):
        rt.add(row.id)
    return rt

def get_company_followed_count(uid):
    res = []
    for row in TDB.engine.execute('select count from user_company_follow_count where user_id = ' + str(uid)):
        res.append(row[0])
    if len(res)  == 0:
        return 0
    else:
        return res[0]

def argsort(seq):
    #http://stackoverflow.com/questions/3382352/equivalent-of-numpy-argsort-in-basic-python/3382369#3382369
    #by unutbu
    return sorted(range(len(seq)), key=seq.__getitem__)


for rec in TDB.engine.execute('select * from user_with_timeline'):
    user_id = rec[0]
    print user_id
    user_tweets = filterEQ(TDB.session, TDB.Tweet, 'user_id', user_id)
    tweet_by_time = ascending(TDB.session, fuse(TDB.session, user_tweets, TDB.Tweet_time, 'id', 'tweet_id'), 'date')
    user_tweets= filterEQ(TDB.session, TDB.Tweet, 'user_id', user_id) #use only those tweets that are present in num_tweets
    user_words = distinct(TDB.session, proj(TDB.session, fuse(TDB.session, user_tweets, TDB.Words_in_tweet,  'id', 'tweet_id'), ['word_id']), ['word_id'])
    num_words = cardinality(TDB.session, user_words)
    num_tweets = cardinality(TDB.session, user_tweets)

    col = 0
    word_to_col = {}
    tweet_to_row = {}
    tweet_to_text = {}
    vocab_list= []
    for w in scan(TDB.session, user_words):
        word_to_col[w.word_id] = col
        col = col + 1
        vocab_list.append(w.word_id)
    vocab = tuple(vocab_list)
    if len(vocab_list)  < 10:
        continue

    titles_list = []
    X = np.zeros((num_tweets, num_words))    
    row = 0
    for t in scan(TDB.session, user_tweets):
        tweet_words = filterEQ(TDB.session, TDB.Words_in_tweet, 'tweet_id', t.id) 
        for tw in scan(TDB.session, tweet_words):
            col = word_to_col[tw.word_id]
            X[row, col] = X[row,col] +1
        titles_list.append(t.id)
        tweet_to_row[t.id] = row
        tweet_to_text[t.id] = t.text
        row=row+1

    titles=tuple(titles_list)     
    num_topics = num_tweets/2
    if num_tweets > 10:
        num_topics = num_tweets/10

    print "num_topics ", num_topics
    model = lda.LDA(n_topics=num_topics, n_iter=500, random_state=1)
    model.fit(X)
    all_topic_words = []
    topic_word = model.topic_word_
    n_top_words = 8

    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        topic_words_list = set()
        for topic in topic_words:
            print topic.encode('utf-8'), " ",
            topic_words_list.add(topic)
        print " "
        all_topic_words.append(topic_words_list)






