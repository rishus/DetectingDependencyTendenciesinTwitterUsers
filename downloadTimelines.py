# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 14:05:41 2014

@author: rishu
"""

import twitter
import TweetDB as TDB
from EpiPipesApi import *
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

def normalize(text):
    return text.lower().replace("\n", " ")


def tokenize(text):
    return filter(lambda i: len(i) > 0, normalize(text).split(' '))

#uoi = ["monique_jean", "erica_stevens" , "natasha_sarah_" , "BandtheBBlog", "mai_hox_" , "MishMreow"  , "hcurriebeauty" , "Robyn_Ashley13" , "vectorvitale", "jazzybaptiste"]

# "ViolentLaFemme"
# "Emma_Frost_Cam",
# "CosmeticAddictn", 

#uoi = TDB.engine.execute("select * from (select count(*) as count, screen_name from user_vs_company, users where users.id = user_vs_company.user_id  group by screen_name order by count desc)  as foo where count > 1 ")
#uoi = scan(TDB.session, TDB.Users)

uoi = TDB.engine.execute("select * from (select count(*) as count, user_id from user_vs_company  group by user_id order by count desc)  as foo where count > 1")
redundant_user = []

for row in uoi:
#    username = row[1] #user.screen_name
    username = row[1]
    page = 1
#    utl = []
    userAddedCtr = 0
    print username
    check_id = TDB.session.query(TDB.User_timeline).filter(TDB.User_timeline.user_id == username).all()
    if (len(check_id) != 0):
        continue
    sq = api.users.lookup(user_id = username)
    if ((sq[0]['protected'] == False) and ((sq[0]['lang'] == 'en') or (sq[0]['lang'] == 'en-gb') or (sq[0]['lang'] == 'en-AU') or (sq[0]['lang'] == 'en-GB') or (sq[0]['lang'] == 'en-au'))):
        if (len(check_id) == 0):
            while page < 17:
        #        statuses = api.statuses.user_timeline(screen_name = username, count = 200, page=page)
                statuses = api.statuses.user_timeline(user_id = username, count = 200, page=page)
                if statuses:
        #             add user details to user table
                    if userAddedCtr == 0:
                        tu= statuses[0]['user']
                        vf = "n"
                        check_id = TDB.session.query(TDB.Users).filter(TDB.Users.id==tu['id']).all()
                        if(len(check_id)== 0):
                            if tu["verified"]:
                                verified = "y"
                            u = TDB.Users(id = tu['id'], 
                                         name=tu['name'], 
                                        screen_name = tu['screen_name'],
                                         location=tu['location'], 
                                         created_at=tu['created_at'],
                                         language = tu['lang'], 
                                         verified = vf,
                                         url = str(tu['url']))
                            TDB.session.add(u)
                            userAddedCtr += 1
                    for tweet in statuses:
        #                utl.append(tweet)
        #                print "(%s) %s" % (tweet["created_at"], tweet["text"])
                        # fill tabe with user id of this user, tweet id of EACH tweet in his/her timeline, and time of tweet.
                        check_id = TDB.session.query(TDB.User_timeline).filter(TDB.User_timeline.user_id == tweet['user']['id']).filter(TDB.User_timeline.tweet_id==tweet['id']).all()
                        if (len(check_id) == 0):
                            ut = TDB.User_timeline(user_id = tweet['user']['id'],
                                                   tweet_id = tweet['id'],
                                                    date_time_str = str(tweet['created_at']))
                            TDB.session.add(ut)
                        # add tweeet details to tweet table
                        check_id = TDB.session.query(TDB.Tweet).filter(TDB.Tweet.id==tweet['id']).all()
                        if(len(check_id) == 0):
                            words = tokenize(tweet['text'])
                            thisisrt = ("1" if 'rt' in words else "0")
                            tw = TDB.Tweet(id=tweet['id'], 
                                           text=tweet['text'], 
                                            created_at= str(tweet['created_at']),
                                            tweet_coords = str(tweet['coordinates']), 
                                            place = str(tweet['place']),
                                            isRT = thisisrt,
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
                                            retweet_count= tweet['retweet_count'])
                            TDB.session.add(tw)
                    
                    TDB.session.commit()
                else:
                    # All done
                    break
                
                page += 1  # next page            
                time.sleep(10)
    else:
        redundant_user.append(username)
        
    time.sleep(5)

                
                
## getting friends of a user
##-----------------------------------------------------------------------
## twitter-friends
## - lists all of a given user's friends (ie, followees)
##-----------------------------------------------------------------------
#username = "ideoforms"
#frnds = api.friends.ids(screen_name = username)
#print "found %d friends" % (len(frnds["ids"]))
#for n in range(0, len(frnds["ids"]), 100):
#    ids = frnds["ids"][n:n+100]
#    sq = api.users.lookup(user_id = ids)   
#    for user in sq:
#        verified = " "
#        if user["verified"]:
#            verified = "*"
#        print " [%s] %s" % (verified, user["screen_name"])



#username = "CosmeticAddictn"
#utl = api.statuses.user_timeline(screen_name = username, count = 200)
#for status in utl:
#    print "(%s) %s" % (status["created_at"], status["text"])
#

