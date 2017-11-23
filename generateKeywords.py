# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 17:43:11 2014

@author: rishu
"""

import twitter
import re
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
eng_stopwords = stopwords.words('english')
from collections import Counter
import time


def processIncomingTweets(res):
    listOfTexts = []
    for i in range(0, len(res['statuses'])):
        userId = res['statuses'][i]['user']['id']
        userName =  res['statuses'][i]['user']['name']
        thisTweetText = res['statuses'][i]['text']
        userLocation = res['statuses'][0]['user']['profile_image_url']
        tweetCreatedAtTime = res['statuses'][0]['created_at']
        profileCreatedAtTime = res['statuses'][0]['user']['created_at']
        listOfTexts.append([userId, userName, thisTweetText, userLocation, tweetCreatedAtTime, profileCreatedAtTime])
       
    return listOfTexts
    
def splitTextIntoSentences(text, sentenceEnders):
    sentenceList = sentenceEnders.split(text)
    return sentenceList


REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "MnswDXsyNIIIIenKUuMtsvp0I"
CONSUMER_SECRET = "0slOLVtrS4Q4e5UwG02LCRfPOmvfA9swzjJN59DbxQ7uF168NL"

OAUTH_TOKEN = "2812137871-bZLxi19xQgA7NMUd030juO7PFGNFXW1lGRw8IM9"
OAUTH_TOKEN_SECRET = "PTcyjTxaK9Fb41DsZOeMCDsFQRgLGh3Ftbw3Zva0wmavq"


auth=twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY , CONSUMER_SECRET)
api=twitter.Twitter(auth=auth)


hashtags = []
user = []
userId = []
contacts = []
urls = []
listOfWords = []
dropped = []
st = LancasterStemmer()
lmtzr = WordNetLemmatizer()
regexp = re.compile("(?P<url>https?://[^\s]+)")
sentenceEnders = re.compile('[,.!?:;]')

#listOfTexts = []
counter = 0
with open('/home/rishu/Courses/CS5525/project/keywordsCosmetics.txt', 'rb') as f:
    for line in f:
        counter += 1
        kw = str(line.split()[0]) 
        print kw
        res = api.search.tweets(q = kw, count=100)
        newList = processIncomingTweets(res)
        listOfTexts += newList
        time.sleep(5)
        
for i in range(0, len(listOfTexts)):
    thisText = listOfTexts[i][2]
    user.append([listOfTexts[i][0], listOfTexts[i][1]])
    userId.append(listOfTexts[i][0])
    if listOfTexts[i][2] in userId:
        print i, ':  name = ', listOfTexts[i][1], 'text = ', thisText
        
    thisTextLower = thisText.lower()
    thisTextSenList = splitTextIntoSentences(thisTextLower, sentenceEnders) 
    thisTextBagOfWords = []    
    for sen in thisTextSenList:
        a = sen.split()
        for word in a:
            if word[0] == '#':
                hashtags.append(word[1:])
            elif word[0] == '@':
                contacts.append(word[1:])
            elif regexp.search(word) is not None:
                urls.append(word)
        
    
    for word in a:
        if word[0] == '#':
            hashtags.append(word[1:])
        elif word[0] == '@':
            contacts.append(word[1:])
        elif regexp.search(word) is not None:
            urls.append(word)
        elif re.match(r'\A[a-z]+[?:!.;]+\Z', word):
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
    
cnt.most_common()[0:30]


cnt = Counter()
for word in listOfWords:
    cnt[word] += 1
    
cnt.most_common()[0:20]

""" version prior to the above version """
#import twitter
#import re
#from nltk.stem.lancaster import LancasterStemmer
#from nltk.stem.wordnet import WordNetLemmatizer
#from nltk.corpus import stopwords
#eng_stopwords = stopwords.words('english')
#from collections import Counter
#import time
#
#
#def processIncomingTweets(res):
#    listOfTexts = []
#    for i in range(0, len(res['statuses'])):
#        listOfTexts.append([res['statuses'][i]['user']['id'], res['statuses'][i]['user']['name'], res['statuses'][i]['text']])
#       
#    return listOfTexts
#
#
#REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
#AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
#ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
#
#CONSUMER_KEY = "MnswDXsyNIIIIenKUuMtsvp0I"
#CONSUMER_SECRET = "0slOLVtrS4Q4e5UwG02LCRfPOmvfA9swzjJN59DbxQ7uF168NL"
#
#OAUTH_TOKEN = "2812137871-bZLxi19xQgA7NMUd030juO7PFGNFXW1lGRw8IM9"
#OAUTH_TOKEN_SECRET = "PTcyjTxaK9Fb41DsZOeMCDsFQRgLGh3Ftbw3Zva0wmavq"
#
#
#auth=twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY , CONSUMER_SECRET)
#api=twitter.Twitter(auth=auth)
#
#
#hashtags = []
#user = []
#userId = []
#contacts = []
#urls = []
#listOfWords = []
#dropped = []
#st = LancasterStemmer()
#lmtzr = WordNetLemmatizer()
#regexp = re.compile("(?P<url>https?://[^\s]+)")
#
#listOfTexts = []
#counter = 0
#with open('/home/rishu/Courses/CS5525/project/listOfKeywords.txt', 'rb') as f:
#    for line in f:
#        counter += 1
#        kw = str(line.split()[0]) 
#        print kw
#        res = api.search.tweets(q = kw, count=100)
#        newList = processIncomingTweets(res)
#        listOfTexts += newList
#        time.sleep(5)
#        
#for i in range(0, len(listOfTexts)):
#    thisText = listOfTexts[i][2]
#    user.append([listOfTexts[i][0], listOfTexts[i][1]])
#    userId.append(listOfTexts[i][0])
#    if listOfTexts[i][2] in userId:
#        print i, ':  name = ', listOfTexts[i][1], 'text = ', thisText
#        
#    a = thisText.lower().split()
#    for word in a:
#        if word[0] == '#':
#            hashtags.append(word[1:])
#        elif word[0] == '@':
#            contacts.append(word[1:])
#        elif regexp.search(word) is not None:
#            urls.append(word)
#        elif re.match(r'\A[a-z]+\Z', word):
#            stemmed = st.stem(word)
#            lemmatized = lmtzr.lemmatize(stemmed)
#            if lemmatized not in eng_stopwords:
#                listOfWords.append(word)
#            else:
#                dropped.append(word)
#        else:
#            dropped.append(word)
#
#
#cnt = Counter()
#for ht in hashtags:
#    cnt[ht] += 1
#    
#cnt.most_common()[1:20]
#
#
#cnt = Counter()
#for word in listOfWords:
#    cnt[word] += 1
#    
#cnt.most_common()[1:20]

