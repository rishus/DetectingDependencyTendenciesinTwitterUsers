# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 18:36:27 2014

@author: rishu
"""

import TweetDB as TDB
from EpiPipesApi import *

count = 0
tws = scan(TDB.session, TDB.Tweet.id)
for tw in tws:
    check_id = TDB.session.query(TDB.Topic_Tweetid).filter(TDB.Topic_Tweetid.tweet_id == tw.id).all()
    count += 1
    print count
    if (len(check_id) == 0):
        u = TDB.Topic_Tweetid(topic = 'cosmetics', tweet_id = tw.id)
        TDB.session.add(u)
        
    print count
    
TDB.session.commit()

