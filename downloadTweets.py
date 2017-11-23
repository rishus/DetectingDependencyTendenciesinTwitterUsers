
#  make sure to run createDB.py before running the for the first time in a given console session

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


# getting all recent (200 max) tweets that correspond to a particular keyword and storing them in the database
#-----------------------------------------------------------------------
# twitter-tweets
# - outputs all tweets, where tweets = a full packet of username, userprofile, 
#       timeoftweet, tweettext, etc etc etc. 
#       and saves them in the database
##-----------------------------------------------------------------------


kws = scan(TDB.session, TDB.keywords)
T = 60 * 60 * 0.1
t = 0
wait =  60 * 0.1

fh = open("downloadsBackup.obj", "ab+")

while t < T:
    for kw in kws:
        if ((kw.topic == 'cosmetics') and (kw.id > 0)):
            print kw.id, " ", kw.priority, " ", kw.keyword
            res = api.search.tweets(q = kw.keyword, count=100)
            pickle.dump(res, fh)
            #    #print res
            for tweet in res['statuses']:
                # user table
#                print 'no'
                tu=tweet['user']
                check_id = TDB.session.query(TDB.User).filter(TDB.User.id==tu['id']).all()
                if(len(check_id)== 0):
                    u = TDB.User(id = tu['id'], 
                                 name=tu['name'], 
                                 location=tu['location'], 
                                 created_at=tu['created_at'],
                                 friends_count=tu['friends_count'], 
                                 followers_count=tu['followers_count'], 
                                 following=tu['following'], )
                    TDB.session.add(u)
        
                # tweet table
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
                                    retweet_count= tweet['retweet_count']  )
                    TDB.session.add(tw)
                
                # tweetid-topic table
                check_id = TDB.session.query(TDB.Topic_Tweetid).filter(TDB.Topic_Tweetid.tweet_id==tweet['id']).all()
                if (len(check_id) == 0):
                    ttid = TDB.Topic_Tweetid(topic = 'cosmetics', tweet_id = tweet['id'])
                    TDB.session.add(ttid)
                
                # network table
                if 'entities' in tweet and len(tweet['entities']['user_mentions']) > 0:
                    user = tweet['user']
                    user_mentions = tweet['entities']['user_mentions']
                    for u2 in user_mentions:
                        check_id = TDB.session.query(TDB.Network).filter(TDB.Network.topic == 'cosmetics').filter(TDB.Network.tweet_id == tweet['id']).filter(TDB.Network.src_id == user['id']).filter(TDB.Network.des_id == u2['id']).all()
                        if (len(check_id) == 0):
#                            print 'yes'
                            nt = TDB.Network(topic = 'cosmetics', 
                                             tweet_id = tweet['id'],
                                             src_id = user['id'],
                                             des_id = u2['id'],
                                             connect = 1)
                            TDB.session.add(nt)
                                                        

            time.sleep(10)
        
    TDB.session.commit()
    print t
    t += wait
    time.sleep(wait)
    

# getting a user's timeline
#-----------------------------------------------------------------------
# twitter-friendship
# - outputs a user's tweets and the times at which the tweet was created.
#   I haven't started saving it in the database yet
##-----------------------------------------------------------------------
#username = "CosmeticAddictn"
#utl = api.statuses.user_timeline(screen_name = username, count = 200)
#for status in utl:
#    print "(%s) %s" % (status["created_at"], status["text"])
#
#
#page = 1
#utl = []
#while page < 16:
#    statuses = api.statuses.user_timeline(screen_name = username, count = 200, page=page)
#    if statuses:
#        for status in statuses:
#            # process status here
#            utl.append(status)
#    else:
#        # All done
#        break
#    page += 1  # next page
    


# getting friends of a user
#-----------------------------------------------------------------------
# twitter-friends
# - lists all of a given user's friends (ie, followees)
#-----------------------------------------------------------------------
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
    
    
# getting followers of a user
#-----------------------------------------------------------------------
# twitter-followers
# - lists all of a given user's followers
#-----------------------------------------------------------------------
#username = "ideoforms"
#followers = []
#followers = api.friends.ids(screen_name = username)


#-----------------------------------------------------------------------
# twitter-friendship
# - outputs details of the relationship between two users.
##-----------------------------------------------------------------------    
#source = "ideoforms"
#target = "lewisrichard"
#frndship = api.friendships.show(source_screen_name = source, target_screen_name = target)
#following = frndship["relationship"]["target"]["following"]
#follows = frndship["relationship"]["target"]["followed_by"]
#print "%s following %s: %s" % (source, target, follows)
#print "%s following %s: %s" % (target, source, following)





    
