# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 18:07:18 2014

@author: rishu
"""

import TweetDB as TDB
import AnalyticsDB as ADB
TDB.Base.metadata.create_all(TDB.engine)
TDB.session.commit()

