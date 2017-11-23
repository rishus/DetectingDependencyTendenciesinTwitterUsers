from datetime import datetime
import datetime
from dateutil import parser
from EpiPipesApi import *
import TweetDB as TDB
import numpy as np
import lda
import sys

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


for rec in TDB.engine.execute('select user_id  from dependency_analysis as D'):
    user_id = rec[0]

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
    if num_topics == 0:
        print>>sys.stdout ("user "+  str(user_id) +  " has zero num_topics")
        continue

    #print "num_topics ", num_topics
    model = lda.LDA(n_topics=num_topics, n_iter=500, random_state=1)
    model.fit(X)
    all_topic_words = []
    topic_word = model.topic_word_
    n_top_words = 8

    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        topic_words_list = set()
        for topic in topic_words:
            #print topic, " ",
            topic_words_list.add(topic)
        #print " "
        all_topic_words.append(topic_words_list)


    doc_topic = model.doc_topic_
    #for i in range(0, num_tweets):
    #    tweet_id = titles[i]
    #    category_id = doc_topic[i].argmax()
    #    if ( len(list(all_topic_words[category_id] & beauty_keywords))  > 3):
    #        print tweet_id, category_id, tweet_to_text[tweet_id].encode('utf-8').strip()

    def is_beauty_tweet(tweet_id):
        row = tweet_to_row[tweet_id]
        category_id = doc_topic[row].argmax()
        if ( len(list(all_topic_words[category_id] & beauty_keywords))  > 2):
            return True
        return False

    def is_shopping_tweet(tweet_id):
        row = tweet_to_row[tweet_id]
        category_id = doc_topic[row].argmax()
        if ( len(list(all_topic_words[category_id] & shopping_keywords))  > 1):
            return True
        return False



    regret_tweets = get_regret_tweets(user_id)
    money_tweets = get_money_tweets(user_id)
    sorrynosorry_tweets = get_sorrynosorry_tweets(user_id)
    user_tweets = filterEQ(TDB.session, TDB.Tweet, 'user_id', user_id)
    tweet_by_time = ascending(TDB.session, fuse(TDB.session, user_tweets, TDB.Tweet_time, 'id', 'tweet_id'), 'date')


    last_beauty_date = datetime.date(year=2001, month=1, day=1)
    last_shop_date = datetime.date(year=2001, month=2, day=1)
    last_money_date = datetime.date(year=2001, month=3, day=1)
    last_regret_date = datetime.date(year=2001, month=4, day=1)
    last_sorrynosorry_date = datetime.date(year=2001, month=5, day=1)

    last_beauty_tweet  = '' 
    last_shop_tweet  = ''
    last_money_tweet = ''
    last_regret_tweet  = ''
    last_sorrynosorry_tweet = ''


    attention_span = 2



    poslabel = ['beauty', 'regret', 'shop', 'money', 'sorrynosorry']
    new_event = 0

    num_companies_followed = 0
    num_beauty_tweets = 0
    num_regret_tweets = 0
    num_shop_tweets  = 0
    num_money_tweets = 0
    num_sorrynosorry_tweets  = 0
    num_other_tweets = 0
    cause_effect = { 'beauty' : { 'beauty' : 0, 'regret' : 0, 'shop' : 0, 'money': 0, 'sorrynosorry' :0  },
                     'regret' : { 'beauty' : 0, 'regret' : 0, 'shop' : 0, 'money': 0, 'sorrynosorry': 0},
                     'shop' : { 'beauty' : 0, 'regret' : 0, 'shop' : 0, 'money': 0, 'sorrynosorry' : 0 },
                     'money' : { 'beauty' : 0, 'regret' : 0, 'shop' : 0, 'money': 0 , 'sorrynosorry': 0},
                     'sorrynosorry' : { 'beauty' : 0, 'regret' : 0, 'shop' : 0, 'money': 0 , 'sorrynosorry': 0},
    }

    fh  = open('report_' + str(user_id) +'.txt', 'w')

    for atweet in scan(TDB.session, tweet_by_time):
        tweet_id = atweet.tweet_id
        if is_beauty_tweet(tweet_id):
            last_beauty_date = atweet.date
            last_beauty_tweet = tweet_to_text[tweet_id]
            fh.write(atweet.date.strftime('%m/%d/%Y') +  " beauty=" + atweet.text.encode('utf-8') +  "\n")
            num_beauty_tweets += 1
            new_event = 1
        if tweet_id in regret_tweets:
            last_regret_date = atweet.date
            last_regret_tweet = tweet_to_text[tweet_id]
            fh.write(atweet.date.strftime('%m/%d/%Y') +  " regret=" + atweet.text.encode('utf-8') + "\n")
            num_regret_tweets += 1
            new_event = 1
        if is_shopping_tweet(tweet_id):
            last_shop_date = atweet.date
            last_shop_tweet = tweet_to_text[tweet_id]
            fh.write(atweet.date.strftime('%m/%d/%Y') +  " shop=" +  atweet.text.encode('utf-8')+ "\n")
            num_shop_tweets +=1
            new_event = 1
        if tweet_id in money_tweets:
            last_money_date = atweet.date
            last_money_tweet = tweet_to_text[tweet_id]
            fh.write(atweet.date.strftime('%m/%d/%Y')+ " money=" +  atweet.text.encode('utf-8'))
            num_money_tweets += 1
            new_event = 1
        if tweet_id in sorrynosorry_tweets:
            last_sorrynosorry_date = atweet.date
            last_sorrynosorry_tweet = tweet_to_text[tweet_id]
            fh.write(atweet.date.strftime('%m/%d/%Y')+ " sorrynosoory="+  atweet.text.encode('utf-8') + "\n" )
            num_sorrynosorry_tweets += 1
            new_event = 1
        all_tweets = [last_beauty_tweet, last_regret_tweet, last_shop_tweet, last_money_tweet, last_sorrynosorry_tweet]
        all_dates = [last_beauty_date, last_regret_date, last_shop_date, last_money_date, last_sorrynosorry_date]
        sorted_idx = argsort(all_dates)
        if new_event == 0:
            num_other_tweets += 1
            continue

        #all_dates.sort()
        for  i in range(0,4):
            #print "at ", i, sorted_idx[i]
            delta = all_dates[sorted_idx[i+1]] - all_dates[sorted_idx[i]] 
            if delta.days < attention_span:
                #print "cause ", poslabel[sorted_idx[i]], " on ", all_dates[sorted_idx[i]] 
                #print "effect ", poslabel[sorted_idx[i+1]], " on ", all_dates[sorted_idx[i+1]] 
                #print "delta ", delta.days
                cause = poslabel[sorted_idx[i]]
                effect=poslabel[sorted_idx[i+1]]
                cause_effect[cause][effect] += 1
                fh.write( "\n \n cause: " + cause + " "  + all_dates[sorted_idx[i]].strftime('%m/%d/%Y') +  " " + all_tweets[sorted_idx[i]].encode('utf-8').strip() +  " effect : "  + effect + "  " +  all_dates[sorted_idx[i+1]].strftime('%m/%d/%Y') +  " " +  all_tweets[sorted_idx[i+1]].encode('utf-8').strip()  + "\n \n")
        new_event = 0

    fh.close()

