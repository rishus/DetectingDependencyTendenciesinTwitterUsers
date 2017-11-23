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
    isdone = []
    for r in  TDB.engine.execute('select * from dependency_analysis where user_id = ' + str(user_id)):
        isdone.append(r[0])

    if len(isdone) != 0:
        print "user ", user_id, " already present"
        continue
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
        print "user ", user_id, " has zero num_topics"
        continue

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

    attention_span = 8



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

    for atweet in scan(TDB.session, tweet_by_time):
        tweet_id = atweet.tweet_id
        if is_beauty_tweet(tweet_id):
            last_beauty_date = atweet.date
            print atweet.date, " beauty=", atweet.text.encode('utf-8')
            num_beauty_tweets += 1
            new_event = 1
        if tweet_id in regret_tweets:
            last_regret_date = atweet.date
            #print atweet.date, " regret=", atweet.text.encode('utf-8')
            num_regret_tweets += 1
            new_event = 1
        if is_shopping_tweet(tweet_id):
            last_shop_date = atweet.date
            print atweet.date, " shop=", atweet.text.encode('utf-8')
            num_shop_tweets +=1
            new_event = 1
        if tweet_id in money_tweets:
            last_money_date = atweet.date
            print atweet.date, " money=", atweet.text.encode('utf-8')
            num_money_tweets += 1
            new_event = 1
        if tweet_id in sorrynosorry_tweets:
            last_sorrynosorry_date = atweet.date
            print atweet.date, " sorrynosoory=", atweet.text.encode('utf-8')
            num_sorrynosorry_tweets += 1
            new_event = 1
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
                print cause,"  ", effect
        new_event = 0



    da = TDB.Dependency_analysis(user_id=user_id, num_biz_following = get_company_followed_count(user_id), 
                            bt = num_beauty_tweets, rt = num_regret_tweets, st=num_shop_tweets, mt = num_money_tweets, snst=num_sorrynosorry_tweets, 
                                 ot=num_other_tweets,
                            btor = cause_effect['beauty']['regret'], 
                            btos = cause_effect['beauty']['shop'], 
                            btom=cause_effect['beauty']['money'], 
                            btosns = cause_effect['beauty']['sorrynosorry'], 
                            stor = cause_effect['shop']['regret'],
                            mtor=cause_effect['money']['regret'], 

    )

    TDB.session.add(da)
    TDB.session.commit()
    #print "company followed count: ", get_company_followed_count(user_id)        
    #for i in range(0,5):
    #    for j in range(i+1, 5):

    # for atweet in scan(tweet_by_time):
    #  isbeauty = classify(beauty_model, atweet)
    #  isshop = classify(shop_model, atweet)
    #  isregret=classify()
