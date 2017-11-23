# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 18:18:17 2014

@author: rishu
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, BigInteger, Integer, String,  PrimaryKeyConstraint

import EpiPipesApi as epi

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
     followers_count = Column(Integer)
     friends_count = Column(Integer)
     location = Column(String)
     following = Column(String)
     name = Column(String)
     created_at = Column(String)
     
     

class Tweet(Base):
    __tablename__='tweet'
    id=Column(BigInteger, primary_key=True)
    text = Column(String)
    retweeted = Column(Boolean)
    created_at = Column(String)
    user_id = Column(BigInteger)
    
    contributors = Column(String)
    truncated = Column(bool)
    in_reply_to_status_id = Column(String)
    in_reply_to_screen_name = Column(String)
    in_reply_to_user_id=Column(String)
    in_reply_to_user_id_str=Column(String)
    in_reply_to_status_id_str=Column(String)
    favorite_count = Column(int)
    source = Column(unicode)
    coordinates=Column(String)
    entities = Column(dict)
    favorited=Column(bool)
    id_str=Column(unicode)
    retweet_count=Column(int)
    retweeted_status=Column(dict)
    user = Column(dict)

class processed_tweet(Base):
    __tablename__ = 'processed_tweet'
    tweet_id = Column(Integer, primary_key=True)
     
class hashtags(Base):
     __tablename__ = 'hashtags'
     id = Column(Integer)
     hashtag = Column(Integer, primary_key=True)
     
class words(Base):
    __tablename__='words'
    word = Column(String, primary_key=True)
    id = Column(Integer)
    
class keywords(Base):
    __tablename__='keywords'
    keyword = Column(String, primary_key=True)
    id = Column(Integer)
    
class words_in_tweet(Base):
    __tablename__='words_in_tweet'
    tweet_id = Column(BigInteger)
    word_id=Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint('tweet_id', 'word_id'),
        {},
    )
class hashtag_in_tweet(Base):
    __tablename__='hashtag_in_tweet'
    hash_id = Column(Integer)
    tweet_id = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint('hash_id', 'tweet_id'),
        {},
    )
    
class network(Base):
    __tablename__='network'
    src_id = Column(Integer)
    des_id = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint('src_id', 'des_id'),
        {},
    )
     
Base.metadata.create_all(engine)

session.commit()