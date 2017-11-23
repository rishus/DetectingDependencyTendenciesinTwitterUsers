# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 15:53:40 2014

@author: rishu
"""

#!/usr/bin/env python -u


#import sys, json, math
from spam_detector_commons import *
import twitter

#model = readModel(sys.argv[1])
#model = readModel('spam_filter_model.txt')
model = readModel('makeupbiz_train.txt')

uoi = ['revlon']
#scan()
marker = []
for username in uoi:
        print username
        page = 1
        while page < 3:
            statuses = api.statuses.user_timeline(screen_name = username, count = 200, page=page)
            for tweet in statuses:
                thisMarker = classify(model, tweet['text'])
                marker.append(thisMarker)
            
            page += 1
                