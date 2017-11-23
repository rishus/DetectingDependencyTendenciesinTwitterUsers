# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 15:35:19 2014

@author: rishu
"""
import twitter
import TweetDB as TDB
import time
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


#uoi = ["bareMinerals" , "revlon" , "ZoyaNailPolish" , "lagirlusa"] #, "askelf" , "NyxCosmetics" , "HourglassMakeup", ] #,"MACcosmetics", "UrbanDecay",, "milanicosmetics", "HourglassMakeup", "Sephora",

uoi = ['tartecosmetics', 'SleekMakeUP', 'HauteLook', 'CHANEL', 'Clinique', 'LOrealParisUSA', 'beautyADDICTS', 
'makeupfact', 'wetnwildbeauty', 'MaryKay', 'Dior', 'neutrogena', 'cleanandclear', 'nycnewyorkcolor',
'tattoodo', 'BareEscentuals', 'UrbanDecay411', 'Sephora_VIB' ]

#'HourglassMakeup', 'sugarpillmakeup', 'ULTA_Beauty', 'birchbox', 'LauraMercier', 'MAKEUPFOREVERUS', 'TooFaced', 'essie', 'MichaelKors', 'BeautyArmy', 'Maybelline'
#'Sephora', 'MACcosmetics', 'UrbanDecay', 'askelf', 'NyxCosmetics', 'NARSissist', 'milanicosmetics', 
#        'thebalm', 'bareMinerals', 'revlon', 'ZoyaNailPolish', 'lagirlusa', 
#'LASplashMakeup', 'lushcosmetics', 'beautylish', 'KorresUSA', 

for brandname in uoi:
    
    print brandname, '\n'
    # this is the user whose friends we will list: get it's own details first
    res = api.statuses.user_timeline(screen_name = brandname, count = 1)
    cid = res[0]['id']
    page = 1
    allfollowers = []
    while page < 4:
        print 'page', page, '\n'

        # perform a basic search
        # twitter API docs: https://dev.twitter.com/docs/api/1/get/friends/ids
        #followers = api.ffollowers.ids(screen_name = username)
        followers_thispage = api.followers.ids(screen_name = brandname, page=page)
        allfollowers += followers_thispage['ids']

        # now we loop through them to pull out more info, in blocks of 100.
        if followers_thispage:
            for n in range(0, len(followers_thispage["ids"]), 100):
                
                ids = followers_thispage["ids"][n:n+100]
                
                # create a subquery, looking up information about these users
                # twitter API docs: https://dev.twitter.com/docs/api/1/get/users/lookup
                print 'starting search', n, 'page ', page
                sq = api.users.lookup(user_id = ids)
                print 'done searching'
                for user in sq:
                    if ((user['protected'] == False) and ((user['lang'] == 'en') or (user['lang'] == 'en-gb') or (user['lang'] == 'en-AU') or (user['lang'] == 'en-GB') or (user['lang'] == 'en-au'))):
                        vf = "n"
                        check_id = TDB.session.query(TDB.Users).filter(TDB.Users.id==user['id']).all()
                        if(len(check_id)== 0):
                            if user["verified"]:
                                vf = "y"
                            u = TDB.Users(id = user['id'], 
                                         name=user['name'], 
                                         screen_name = user['screen_name'],
                                         location=user['location'], 
                                         created_at=user['created_at'],
                                         language = user['lang'], 
                                         verified = vf,
                                         url = str(user['url']))
                            TDB.session.add(u)
                        else:
                            print 'already present in users table'
                            
                        check_id = TDB.session.query(TDB.User_vs_company).filter(TDB.User_vs_company.user_id==user['id']).filter(TDB.User_vs_company.company_id == cid).all()
                        if (len(check_id) == 0):
                            uc = TDB.User_vs_company(user_id = user['id'],
                                                     company_id = cid,
                                                     company_screen_name = brandname)

                            TDB.session.add(uc)
                        
                    else:
                        print 'user protected is ', user['protected'], 'language is', user['lang']
                
                TDB.session.commit()
                time.sleep(15)
                    # now print out user info, starring any users that are Verified.
#                            print " [%s] %25s %25s" % (vf, user['name'], user["screen_name"])
                    
        else:
            break
        
        page += 1
        time.sleep(30)
        
    
    # tell the user how many friends we've found.
    # note that the twitter API will NOT immediately give us any more
    # information about friends except their numeric IDs...
    print "found %d followers" % len(allfollowers)



#for id in ids:
#            sq = api.users.lookup(user_id = id)
#            print sq[0]['name']
#            verified = " "
#            if sq[0]["verified"]:
#                verified = "*"
#                
#            # now print out user info, starring any users that are Verified.
#            print " [%s] %s" % (verified, sq[0]["screen_name"])







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