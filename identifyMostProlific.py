# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 08:54:14 2014

@author: rishu
"""

import pygal
import TweetDB as TDB
from EpiPipesApi import *

pytweets = []
users = TDB.scan(TDB.session, TDB.User)
# Use Python collection for counting frequency

user_count = Counter()
for usr in users:
    user_count[usr['id']] += 1


# Prepare the SVG Plot

user_tweet = fuse(TDB.session, TDB.User, TDB.Tweet_mirror, 'id', 'user_id')
barplot = pygal.HorizontalBar( style=pygal.style.SolidColorStyle )

topnum = 10
for i in range(topnum):
    barplot.add( user_count.most_common(topnum)[i][0], \
              [ { 'value': user_count.most_common(topnum)[i][1], \
                  'label':user_count.most_common(topnum)[i][0]} ] )

barplot.config.title = barplot.config.title= "Top " + str(topnum) + " Most Prolific Tweeters"
barplot.config.legend_at_bottom=True

barplot.render_to_file("Top_Tweeters.svg")