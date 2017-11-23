# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 16:42:02 2014

@author: rishu
"""


import twitter
import TweetDB as TDB
from EpiPipesApi import *

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "MnswDXsyNIIIIenKUuMtsvp0I"
CONSUMER_SECRET = "0slOLVtrS4Q4e5UwG02LCRfPOmvfA9swzjJN59DbxQ7uF168NL"

OAUTH_TOKEN = "2812137871-bZLxi19xQgA7NMUd030juO7PFGNFXW1lGRw8IM9"
OAUTH_TOKEN_SECRET = "PTcyjTxaK9Fb41DsZOeMCDsFQRgLGh3Ftbw3Zva0wmavq"


auth=twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY , CONSUMER_SECRET)
api=twitter.Twitter(auth=auth)


uoi = scan(TDB.session, TDB.Users)

for user in uoi:
    uid = user.id
    frnds = api.friends.ids(user_id = user.id)  # these are ids of the people that this user is following
    check_id = TDB.session.query(TDB.User_vs_class).filter(TDB.User_vs_class.user_id == uid).all()
    if (len(check_id) == 0):
        if ((len(frnds["ids"]) > 2500) and (len(frnds["ids"]) < 5000000)):
            uc = TDB.User_vs_class(user_id = uid, followers_count = len(frnds), cl = 'B')
        elif (len(frnds["ids"]) >= 5000000):
            uc = TDB.User_vs_class(user_id = uid, followers_count = len(frnds), cl = 'C')
        else:
            uc = TDB.User_vs_class(user_id = uid, followers_count = len(frnds), cl = 'S')
            
        TDB.session.add(uc)
                
    if (len(frnds["ids"]) < 2500):
        for n in range(0, len(frnds["ids"]), 100):
            frnds_ids = frnds["ids"][n:n+100]
            sq = api.users.lookup(user_id = frnds_ids)   # this is a list of profile-infos of the friends listed in ids list
            for frnd in sq:
                vf = 'n'
                if frnd['followers_count'] >= 5000000:
                    # put this in the celebrity table
                    check_id = TDB.session.query(TDB.Celebrities).filter(TDB.Celebrities.celeb_id==frnd['id']).all()
                    if(len(check_id)== 0):
                        if frnd["verified"]:
                            vf = "y"
                        cu = TDB.Celebrities(celeb_id = frnd['id'], 
                                           celeb_followers_count = frnd['followers_count'],
                                           celeb_name=frnd['name'], 
                                           celeb_screen_name = frnd['screen_name'],
                                           celeb_location=frnd['location'], 
                                           celeb_created_at=frnd['created_at'],
                                           celeb_language = frnd['lang'], 
                                           celeb_verified = vf,
                                           celeb_url = str(frnd['url']))
                        TDB.session.add(cu)
                    
                elif ((frnd['followers_count'] > 2500) and (frnd['followers_count'] < 5000000)):
                    
                    # business. put this in the business list
                    check_id = TDB.session.query(TDB.Businesses).filter(TDB.Businesses.biz_id==frnd['id']).all()
                    if(len(check_id)== 0):
                        if frnd["verified"]:
                                vf = "y"
                        bu = TDB.Businesses(biz_id = frnd['id'], 
                                            biz_followers_count = frnd['followers_count'],
                                            biz_name=frnd['name'], 
                                            biz_screen_name = frnd['screen_name'],
                                            biz_location=frnd['location'], 
                                            biz_created_at=frnd['created_at'],
                                            biz_language = frnd['lang'], 
                                            biz_verified = vf,
                                            biz_url = str(frnd['url']))
                        TDB.session.add(bu)
                else:
                    print frnd['screen_name'] , " : single user" , "followers_count : " , frnd['followers_count']
                
            time.sleep(12)
    TDB.session.commit()

                