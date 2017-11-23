# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 06:47:26 2014

@author: rishu
"""

import twitter
import TweetDB as TDB
#from EpiPipesApi import *
import time
import pickle
import datetime
    
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "MnswDXsyNIIIIenKUuMtsvp0I"
CONSUMER_SECRET = "0slOLVtrS4Q4e5UwG02LCRfPOmvfA9swzjJN59DbxQ7uF168NL"

OAUTH_TOKEN = "2812137871-bZLxi19xQgA7NMUd030juO7PFGNFXW1lGRw8IM9"
OAUTH_TOKEN_SECRET = "PTcyjTxaK9Fb41DsZOeMCDsFQRgLGh3Ftbw3Zva0wmavq"


auth=twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY , CONSUMER_SECRET)
api=twitter.Twitter(auth=auth)


date0 = datetime.date(2007, 1, 1)

# getting a user's timeline
#-----------------------------------------------------------------------
# twitter-friendship
# - outputs a user's tweets and the times at which the tweet was created.
#   I haven't started saving it in the database yet
##-----------------------------------------------------------------------

uoi = ["CosmeticAddictn", "monique_jean", "erica_stevens" , "natasha_sarah_" , "BandtheBBlog", "mai_hox_" 
        "MishMreow"  , "hcurriebeauty" , "Robyn_Ashley13" , "vectorvitale", "jazzybaptiste"]

#"Emma_Frost_Cam"

for user in uoi:
    username = user
    page = 1
    utl = []
    while page < 10:
        statuses = api.statuses.user_timeline(screen_name = username, count = 200, page=page)
        if statuses:
            for tweet in statuses:
                utl.append(tweet)
                print "(%s) %s" % (tweet["created_at"], tweet["text"])
                # fill tabe with user id of this user, tweet id of EACH tweet in his/her timeline, and time of tweet.
                check_id = TDB.session.query(TDB.User_timeline).filter(TDB.User_timeline.user_id == tweet['user']['id']).filter(TDB.User_timeline.tweet_id==tweet['id']).all()
                if (len(check_id) == 0):
                    ut = TDB.User_timeline(user_id = tweet['user']['id'],
                                           tweet_id = tweet['id'],
                                            date_time_str = str(tweet['created_at']),
                                            topic = 'cosmetics')
                    TDB.session.add(ut)
                # add tweeet details to tweet table
                check_id = TDB.session.query(TDB.Tweet).filter(TDB.Tweet.id==tweet['id']).all()
                if(len(check_id) == 0):
                    tw = TDB.Tweet(id=tweet['id'], 
                                   text=tweet['text'], 
                                    created_at= str(tweet['created_at']),
                                    tweet_coords = str(tweet['coordinates']), 
                                    place = str(tweet['place']),
                                    retweeted=tweet['retweeted'], 
                                    user_id=tweet['user']['id'], 
                                    language = tweet['lang'],
                                    contributors = tweet['contributors'],
                                    truncated = tweet['truncated'],
                                    in_reply_to_status_id = tweet['in_reply_to_status_id'],
                                    in_reply_to_screen_name = tweet['in_reply_to_screen_name'],
                                    in_reply_to_user_id= tweet['in_reply_to_user_id'],
                                    in_reply_to_user_id_str= tweet['in_reply_to_user_id_str'],
                                    in_reply_to_status_id_str= tweet['in_reply_to_status_id_str'],
                                    favorite_count = tweet['favorite_count'],
                                    source = tweet['source'],
                                    favorited= tweet['favorited'],
                                    id_str= tweet['id_str'],
                                    retweet_count= tweet['retweet_count'],
                                    isRT = tweet[''] )
                    TDB.session.add(tw)
            
            TDB.session.commit()
        else:
            # All done
            break
        page += 1  # next page
    


#username = "CosmeticAddictn"
#utl = api.statuses.user_timeline(screen_name = username, count = 200)
#for status in utl:
#    print "(%s) %s" % (status["created_at"], status["text"])
#


    