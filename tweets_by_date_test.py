from datetime import datetime
from dateutil import parser
from EpiPipesApi import *
import TweetDB as TDB
import numpy as np
import lda
#for each timeline
#order tweets by date



user_id = 336092289
user_tweets = filterEQ(TDB.session, TDB.Tweet, 'user_id', user_id)
tweet_by_time = ascending(TDB.session, fuse(TDB.session, user_tweets, TDB.Tweet_time, 'id', 'tweet_id'), 'date')
for atweet in scan(TDB.session, tweet_by_time):
    print atweet.date, " ", atweet.text.encode('utf-8'), atweet.tweet_id
