# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 20:14:13 2014

@author: rishu
"""

from collections import defaultdict
from spam_detector_commons import *
import twitter
import time
import os
import TweetDB as TDB

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "MnswDXsyNIIIIenKUuMtsvp0I"
CONSUMER_SECRET = "0slOLVtrS4Q4e5UwG02LCRfPOmvfA9swzjJN59DbxQ7uF168NL"

OAUTH_TOKEN = "2812137871-bZLxi19xQgA7NMUd030juO7PFGNFXW1lGRw8IM9"
OAUTH_TOKEN_SECRET = "PTcyjTxaK9Fb41DsZOeMCDsFQRgLGh3Ftbw3Zva0wmavq"


auth=twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY , CONSUMER_SECRET)
api=twitter.Twitter(auth=auth)

def normalize(text):
    return text.lower().replace("\n", " ")


def tokenize(text):
    return filter(lambda i: len(i) > 0, normalize(text).split(' '))

D = set()
wordProb = {'B':defaultdict(int), 'G': defaultdict(int)}
wordSize = {'B': 0, 'G': 0}
docCount = {'B': 0, 'G': 0}


def feedModel(allUsernames, cla):
    global docCount, D, wordProb, wordSize
    for username in allUsernames:
        print username
        page = 1
        while page < 2:
            statuses = api.statuses.user_timeline(screen_name = username, count = 200, page=page)
            if statuses:
                for tweet in statuses:
                    klass = cla #spammer.cl  #parts[0]
                    attr =  tweet['text']     #json.loads(parts[1])
                    docCount[klass] += 1
                    print docCount[klass]
                    for w in getFeatures(attr):
                        D.add(w)
                        wordProb[klass][w] += 1
                        wordSize[klass] += 1
                    print attr
                    
                    # also, make sure to save the tweets in beautybiz_training_tweet table and, probably, in vocab in beautybiz_training_vocab table
                    check_id = TDB.session.query(TDB.Beautybiz_training_tweet).filter(TDB.Beautybiz_training_tweet.tweet_id==tweet['id']).all()
                    irtw = tokenize(tweet['text'])
                    thisisrt = ("1" if 'rt' in irtw else "0")
                    if (len(check_id) == 0):
                        tw = TDB.Beautybiz_training_tweet(tweet_id=tweet['id'],
                                                          text = tweet['text'],
                                                          created_at = str(tweet['created_at']),
                                                          tweet_coords=str(tweet['coordinates']),      # latitude-longitude of tweet location (nullifiable)
                                                          place = str(tweet['place']),           # bounding box for places associated with/ mentioned in the tweet location as reported by the device (nullifiable)
                                                          isRT = thisisrt,
                                                          retweeted = tweet['retweeted'],
                                                          user_id = tweet['user']['id'],     # unique   
                                                          language = tweet['lang'],
                                                          cl = cla )
                        TDB.session.add(tw)
                    
            else:
                # All done
                TDB.session.commit()
                break
            page += 1  # next page            
            time.sleep(10)
        TDB.session.commit()

modelFileName = 'makeupbiz_train.txt'

if os.path.isfile(modelFileName):
    (docCount, wordSize, wordProb, D) = readModel(modelFileName)
else:
    D = set()
    wordProb = {'B':defaultdict(int), 'G': defaultdict(int)}
    wordSize = {'B': 0, 'G': 0}
    docCount = {'B': 0, 'G': 0}




MakeupUsernames = []
with open('/home/rishu/Courses/CS5525/project/makeupBrands.txt', 'rb') as f:
    for line in f:
        lkw = line.split()
        print lkw
        MakeupUsernames.append(lkw[0])

NonMakeupUsernames = []
with open('/home/rishu/Courses/CS5525/project/nonMakeupBiz.txt', 'rb') as f:
    for line in f:
        lkw = line.split()
        print lkw
        NonMakeupUsernames.append(lkw[0])

feedModel(MakeupUsernames, 'G')
feedModel(NonMakeupUsernames, 'B')

writeModel(modelFileName, docCount, wordSize, wordProb, D)
