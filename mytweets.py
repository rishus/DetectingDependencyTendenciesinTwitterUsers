# -*- encoding: utf-8 -*-

#from __future__ import unicode_literals
#import requests
#from requests_oauthlib import OAuth1
#from urlparse import parse_qs
import twitter


import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, BigInteger, String, Boolean
conn_str='postgresql+psycopg2://localhost:' + str(5432) + '/postgres'

engine=create_engine(conn_str)
# Name the session and bind the engine to the session
Session = sessionmaker()
Session.configure(bind=engine)
session=Session()
Base = declarative_base()

class User(Base):
     __tablename__ = 'users'
     id = Column(BigInteger, primary_key=True)
     followers_count=Column(Integer)
     friends_count=Column(Integer)
     location=Column(String)
     following=Column(String)
     name=Column(String)
     created_at=Column(String)

class Tweet(Base):
    __tablename__='tweet'
    id=Column(BigInteger, primary_key=True)
    text=Column(String)
    retweeted=Column(Boolean)
    created_at=Column(String)
    user_id=Column(BigInteger)
    
class keywords:
    __tablename__ = 'keywords'
    keyword = Column(String, primary_key=True)
    priority = Column(Integer) 
    
    
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "MnswDXsyNIIIIenKUuMtsvp0I"
CONSUMER_SECRET = "0slOLVtrS4Q4e5UwG02LCRfPOmvfA9swzjJN59DbxQ7uF168NL"

OAUTH_TOKEN = "2812137871-bZLxi19xQgA7NMUd030juO7PFGNFXW1lGRw8IM9"
OAUTH_TOKEN_SECRET = "PTcyjTxaK9Fb41DsZOeMCDsFQRgLGh3Ftbw3Zva0wmavq"


auth=twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY , CONSUMER_SECRET)
api=twitter.Twitter(auth=auth)
res1 = api.search.tweets(q='#cosmetics', count=100)
res2 = api.search.tweets(q='#makeup', count=100)
res3 = api.search.tweets(q='#beauty', count=100)
res4 = api.search.tweets(q='#lipstick', count=100)
res6 = api.search.tweets(q='#sexy', count=100)
res7 = api.search.tweets(q='#mua', count=100)
res = api.search.tweets(q='#care', count=100)
#statuses = api.GetUserTimeline(user)

for tweet in res['statuses']:
    tu=tweet['user']

    check_id = session.query(User).filter(User.id==tu['id']).all()
    if(len(check_id)== 0):
        u = User(id = tu['id'], followers_count=tu['followers_count'], friends_count=tu['friends_count'], location=tu['location'], following=tu['following'], name=tu['name'], created_at=tu['created_at'] )
        session.add(u)

    check_id = session.query(Tweet).filter(Tweet.id==tweet['id']).all()
    if(len(check_id) == 0):
        tw = Tweet(id=tweet['id'], text=tweet['text'], retweeted=tweet['retweeted'], created_at=tweet['created_at'], user_id=tu['id'])
        session.add(tw)
    #print 'text = ', tweet['text']    print 'user = ', tweet['user']['name']  print 'tweet = ', tweet['text']  print 'time = ', tweet['created_at']  print '\n\n'
        
    #check_id = session.query(keywords).filter(User.id==tu['id']).all()


session.commit()

listOfTexts = []
""" Step 1: From all tweets, collect text from each tweet """
for i in range(0, len(res['statuses'])):        
    listOfTexts.append(res['statuses'][i]['text'])


