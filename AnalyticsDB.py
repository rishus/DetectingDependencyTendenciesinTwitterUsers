# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 14:21:00 2014

@author: rishu
"""
from TweetDB import Base, Integer, BigInteger, String,Column, PrimaryKeyConstraint

class Usertimeline_category(Base):
    __tablename__='usertimeline_category'
    user_id = Column(BigInteger )
    category_id = Column(Integer)
    topic= Column(String)
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'category_id', 'topic'),
        {},
    )

class Tweet_category(Base):
    __tablename__='tweet_category'
    tweet_id = Column(BigInteger)
    category_id = Column(BigInteger)
    __table_args__ = (
        PrimaryKeyConstraint('tweet_id', 'category_id'),
        {},
    )