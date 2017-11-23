# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 21:17:39 2014

@author: rishu
"""
#from urllib.parse import urlparse

import re
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
eng_stopwords = stopwords.words('english')
from collections import Counter

def processIncomingTweets(res):
    listOfTexts = []
    for i in range(0, len(res['statuses'])):
        listOfTexts.append([res['statuses'][i]['user']['id'], res['statuses'][i]['user']['name'], res['statuses'][i]['text']])
        
    return listOfTexts
    

def processTweet(tweet_obj):
    tweet = tweet_obj.text
    a = tweet.lower().split()
    for word in a:
        if word[0] == '#':
            hashtags.append(word[1:])
        elif word[0] == '@':
            contacts.append(word[1:])
        elif regexp.search(word) is not None:
            urls.append(word)
        elif re.match(r'\A[a-z]+\Z', word):
            stemmed = st.stem(word)
            lemmatized = lmtzr.lemmatize(stemmed)
            if lemmatized not in eng_stopwords:
                listOfWords.append(word)
            else:
                dropped.append(word)
        else:
            dropped.append(word)     # note: many seemingly good words, eg. vacancies, 
        

regexp = re.compile("(?P<url>https?://[^\s]+)")

""" Step 1-2: From the tweeted texts collected, collect actual message and hash tags separately """
hashtags = []
user = []
userId = []
contacts = []
urls = []
listOfWords = []
dropped = []
st = LancasterStemmer()
lmtzr = WordNetLemmatizer()
listOfTexts = processIncomingTweets(res)
for i in range(0, len(listOfTexts)):
    thisText = listOfTexts[i][2]
    user.append([listOfTexts[i][0], listOfTexts[i][1]])
    userId.append(listOfTexts[i][0])
    if listOfTexts[i][2] in userId:
        print i, ':  name = ', listOfTexts[i][1], 'text = ', thisText
        
    a = thisText.lower().split()
    for word in a:
        if word[0] == '#':
            hashtags.append(word[1:])
        elif word[0] == '@':
            contacts.append(word[1:])
        elif regexp.search(word) is not None:
            urls.append(word)
        elif re.match(r'\A[a-z]+\Z', word):
            stemmed = st.stem(word)
            lemmatized = lmtzr.lemmatize(stemmed)
            if lemmatized not in eng_stopwords:
                listOfWords.append(word)
            else:
                dropped.append(word)
        else:
            dropped.append(word)


cnt = Counter()
for ht in hashtags:
    cnt[ht] += 1
    
cnt.most_common()[1:10]


cnt = Counter()
for word in listOfWords:
    cnt[word] += 1
    
cnt.most_common()[1:10]

