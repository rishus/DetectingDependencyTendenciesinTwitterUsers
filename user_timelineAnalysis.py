# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 22:14:55 2014

@author: rishu
"""

from datetime import datetime
from dateutil import parser
from EpiPipesApi import *
import TweetDB as TDB
ctr = 1

for rec in TDB.engine.execute('select * from tweet_time_tmp'):
 #for rec in TDB.session.query(TDB.User_timeline).yield_per(10000):
dt = parser.parse(rec.date_time_str)
d = TDB.Tweet_time(tweet_id= rec.tweet_id, date=dt)
# c = cardinality(TDB.session, filterEQ(TDB.session, TDB.Tweet_time, 'tweet_id', rec.tweet_id))
 #print rec.tweet_id, " ", c
 c = 0
 if c == 0:
  TDB.session.add(d)
  ctr = ctr + 1
  print ctr
 if ctr% 10000 == 0:
   TDB.session.commit()
   print ctr

TDB.session.commit()

#for each timeline
#order tweets by date
# user_tweets = filterEQ(TDB.session, TDB.tweet, 'user_id', 3243242)
# tweet_by_time = ascending(TDB.session, fuse(TDB.session, user_tweets, TDB.Tweet_time, 'id', 'tweet_id'), 'date')

# for atweet in scan(tweet_by_time):
#  isbeauty = classify(beauty_model, atweet)
#  isshop = classify(shop_model, atweet)
#  isregret=classify()
