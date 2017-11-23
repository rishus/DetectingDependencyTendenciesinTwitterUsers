# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 14:09:30 2014

@author: rishu
"""

import datetime
from spam_detector_classify import *

def getMonth(text):
    return {
    'jan' : 1,
    'feb' : 2,
    'march' : 3,
    'apr' : 4,
    'may' : 5,
    'june' : 6,
    'july' : 7,
    'aug' : 8,
    'sept' : 9,
    'oct' : 10,
    'nov' : 11,
    'dec' : 12 }[text]
    
def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1

import twitter
    
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "MnswDXsyNIIIIenKUuMtsvp0I"
CONSUMER_SECRET = "0slOLVtrS4Q4e5UwG02LCRfPOmvfA9swzjJN59DbxQ7uF168NL"

OAUTH_TOKEN = "2812137871-bZLxi19xQgA7NMUd030juO7PFGNFXW1lGRw8IM9"
OAUTH_TOKEN_SECRET = "PTcyjTxaK9Fb41DsZOeMCDsFQRgLGh3Ftbw3Zva0wmavq"


auth=twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY , CONSUMER_SECRET)
api=twitter.Twitter(auth=auth)


username = 'monique_jean'
# check number of followers
userinfo = api.statuses.user_timeline(screen_name = username, count = 2, page=1)

numFollowees =  userinfo[0]['user']['friends_count']
numFollowers =  userinfo[0]['user']['followers_count']


# mark the number of followers
if numFollowers > 2500:
    print 'user is probably not a single user anyways'    
    return

# if single single, then check timeline
profile_created = userinfo[0]['user']['created_at']
c = profile_created.split()
date = c[2]
month = getMonth(c[1].lower())
year = c[5]
date0 = datetime.date(2009, 1, 1)
page = 1
t = []
t_matrix = []
userTimeline = []
while page < 17:    
    userTimeline.append(api.statuses.user_timeline(screen_name = username, count = 200, page=page))
    page += 1
    time.sleep(10)
    
tmp = np.zeros((1, 10))
for tweet in userTimeline:
    text = str(tweet['text'])
    b =  str(tweet['created_at'])    
    c = b.split()
    date = c[2]
    month = getMonth(c[1].lower())
    year = c[5]
    
    tmp[0] = (datetime.datetime(int(year), month, int(date)).date() - date0).days
    t.append(tmp)
    
    # check spam or not: mark the time-series matrix
    
    isSpam = spam_classifer(text)
    if (isSpam == 'B'):
        continue
    
    # check beauty or not: mark the time-series matrix
    isMakeup = spam_detector_classify(text)
    t[2] = 1
    if isMakeup:
        # check money involved or not. If yes, count money if possible. Use sql query for this
        money_involved = '$' in text
        if money_involved:
            t[3] = 1
            t[4] = text.split()[index_containing_substring(text.split(), '$')]
        
        # may be try catching some other phrases used.

    # check regret or not regret: if regret, check the tweet for shopping/makeup and also the surrounding tweets
    isPreviousTweetMakeup = t_matrix['prev', 2]
    isRegret = spam_classifier('text')
    if (isRegret and (isMakeup | isPreviousTweetMakeup)):
            t[5] = 1
            
    # check sorrynotsorry or not: if yes, check the surrounding tweets
    isSorryNotSorry = spamClasifier('text')
    if (isSorryNotSorry  and (isMakeup | isPreviousTweetMakeup)):
        t[6] = 1
        
    

# classify the followees
makeupFollowees = []
for fol in makeupFollowees:
    ratio = makeupFollowees/(len(followees))


