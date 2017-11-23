from collections import defaultdict
from beauty_detector_commons import *
import TweetDB as TDB

D = set()
wordProb = {'B':defaultdict(int), 'G': defaultdict(int)}
wordSize = {'B': 0, 'G': 0}
docCount = {'B': 0, 'G': 0}


for rec in TDB.engine.execute('select * from beautytweet_training_tweet  limit 4277'):
    klass = 'B'
    attr =  rec.text     
    docCount[klass] += 1
    #print rec.text
    for w in getFeatures(attr):
        D.add(w)
        wordProb[klass][w] += 1
        wordSize[klass] += 1

for rec in TDB.engine.execute('select * from beauty_tweets_v3 where count > 3'):
    klass = 'G'
    attr =  rec.text     
    docCount[klass] += 1
    for w in getFeatures(attr):
        D.add(w)
        wordProb[klass][w] += 1
        wordSize[klass] += 1


for rec in TDB.engine.execute('select * from (select id, text, count(word_id) as count from tweet, words_in_tweet where tweet_id = id and words_in_tweet.word_id in (select keyword from keywords) group by id) as foo where id not in (select id from beauty_tweets_v3 where count > 3) and count > 3'):
    klass = 'G'
    attr =  rec.text     
    docCount[klass] += 1
    for w in getFeatures(attr):
        D.add(w)
        wordProb[klass][w] += 1
        wordSize[klass] += 1


model = (docCount, wordSize, wordProb, D)
ctr = 0
for rec in TDB.engine.execute('select * from beautytweet_training_tweet order by random() limit 4000'):
    pc = classify(model, rec.text)
    if (pc != 'B'):
        ctr  = ctr + 1
        print ctr, " beauty ", rec.text.encode('utf-8')
    #else:
    #    print "is beauty ", rec.text.encode('utf-8')

ctr = 0

for rec in TDB.engine.execute('select * from beauty_tweets_v3   order by random() limit 4000'):
    pc = classify(model, rec.text)
    if (pc != 'G'):
        ctr  = ctr + 1
        print ctr, " Not beauty ", rec.text.encode('utf-8')
    #else:
    #    print "is beauty ", rec.text.encode('utf-8')

