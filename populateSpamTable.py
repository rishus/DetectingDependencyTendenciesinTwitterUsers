# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 13:47:44 2014

@author: rishu
"""

# actually i did this directly in postgres using the following command:
#insert into spam_tweet_table select distinct tweet.id, tweet.text, 'spam', users.id, users.name from words_in_tweet, tweet, users where word_id in (select word_id from spam_words) and words_in_tweet.tweet_id = tweet.id and tweet.user_id = users.id;

import TweetDB as TDB
from EpiPipesApi import *

#count = 0
#tws = scan(TDB.session, TDB.Tweet.id)
#for tw in tws:
#    check_id = TDB.session.query(TDB.Topic_Tweetid).filter(TDB.Topic_Tweetid.tweet_id == tw.id).all()
#    count += 1
#    print count
#    if (len(check_id) == 0):
#        u = TDB.Topic_Tweetid(topic = 'cosmetics', tweet_id = tw.id)
#        TDB.session.add(u)
#        
#    print count
#    
#TDB.session.commit()


uoi = ["monique_jean"]
for username in uoi:
    page = 1
    while page < 3:
        statuses = api.statuses.user_timeline(screen_name = username, count = 200, page=page)
        if statuses:
            for tweet in statuses:
                this_cl = 'B'
                check_id = TDB.session.query(TDB.Beauty_tweet).filter(TDB.Beauty_tweet.tweet_id == tweet['id']).all()
                if (len(check_id) == 0):
                    print tweet['text']
                    isCosTw = raw_input('Is this tweet a cosmetics tweet? : ')
                    print 'ur answer  is :   ', isCosTw 
                    if ((isCosTw == 'n') or (isCosTw == 'no')):
                        print 'ur answer  is :   ', isCosTw 
                        this_cl = 'O'
                    
                    print 'this_cl = ' , this_cl
                    # fill this tweet in beauty_tweet table:
                    bt = TDB.Beauty_tweet(tweet_id = tweet['id'],
                          text = tweet['text'],
                          cl = this_cl,
                          user_id = tweet['user']['id'],
                          user_screen_name = username)
     
                   
                    TDB.session.add(bt)
                    TDB.session.commit()


# Alternatively:
#tl = TDB.scan(TDB.session, TDB.User_timeline)
#for user in uoi:
#    # get his uid
#    # get his tids
#    for tid in tids:
        
    
                    
#    for tw in tweets:
#        print " happy anniversary hon!!! was beautiful!!!! "
#        isCosTw = raw_input('Is this tweet a cosmetics tweet?   : ')
#        print 'ur answer  is :   ', isCosTw 
        
#        # fill this tweet in beauty_tweet table:
#        bt = TBD.Beauty_tweet(tweet_id = tw.id,
#                              text = tw.text,
#                              cl = 'B',
#                              user_id = uid,
#                              user_screen_name = uoi)


    