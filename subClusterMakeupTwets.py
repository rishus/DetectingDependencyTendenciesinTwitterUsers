# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 09:19:44 2014

@author: rishu
"""

import AnalyticsDB as ADB
import TweetDB as TDB
from EpiPipesApi import *
import lda
import numpy as np

uoi = TDB.engine.execute("select  distinct  A.id, A.text from tweet as A, tweet_category as B, usertimeline_category C where A.id = B.tweet_id and A.user_id = C.user_id and C.topic in (select keyword from keywords) and B.category_id = C.category_id and C.topic != 'photo';")

