# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 22:01:42 2014

@author: rishu
"""

import re
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
eng_stopwords = stopwords.words('english')
import myStopwords
for sw in myStopwords.STOP_WORDS:
    if sw not in eng_stopwords:
        eng_stopwords.append(sw)



def filter_words(listOfWords):
    listOfWords_content = []
    listOfWords_dropping = []
    for entry in listOfWords:
        if len(entry) <= 1:
            listOfWords_dropping.append(entry)
        elif re.match(r'\A[a-z]+\Z', entry):
            if entry not in eng_stopwords:
                listOfWords_content.append(entry)
            else:
                listOfWords_dropping.append(entry)
        else:
            if re.match(r'\A_[a-z]+_\Z',entry):
                listOfWords_content.append(entry[1:-1])
            elif re.match(r'\A[a-z]+_\Z',entry):
                listOfWords_content.append(entry[0:-1])
            elif re.match(r'\A_[a-z]+\Z',entry):
                listOfWords_content.append(entry[1:])
            elif re.match(r'\w+(?:-\w+)+', entry):
                tmp = entry.replace('-','')
                listOfWords_content.append(tmp)
           # else:
                #print entry
    return [listOfWords_content, listOfWords_dropping]
    
def createBagOfWords(origListOfWords):
    st = LancasterStemmer()
    tmp3 = [st.stem(i) for i in origListOfWords]
    lmtzr = WordNetLemmatizer()
    tmp4 = [lmtzr.lemmatize(i) for i in tmp3]
    [tmp5, tmp6] = filter_words(tmp4)
    return tmp5
    
def processTweet(thisText, regexp, urldelims, sentenceEnders):
    hashtags = []
    contacts = []
    urls = []
    dropped = []
    chh = 0

    allWords = thisText.lower().split()  # splits based on white spaces. and only based on white spaces. puntuations are retained.
    finalWordList = []       
    for word in allWords:
        if word == 'rt':
            dropped.append(word)
        #" get hashtags "
        elif word[0] == '#':               
            hashtags.append(word)
        #"get contacts "
        elif word[0] == '@':
            contacts.append(word)
        #" get urls"
        elif regexp.search(word) is not None:
            urls.append(word)
            
        # get rid of apostrophes
        elif (word[-3:] == "n't") | (word[-3:]=="'ve") :
            word1 = word[0:-3]
            word2 = word[0:-2]
            if (word1 in eng_stopwords) | (word2 in eng_stopwords):
                dropped.append(word)
            else:
                finalWordList.append(word1) # No!! put word1 through the usual filter n then decide
    
        elif word[-3:] == "'re":
            word1 = word[0:-3]
            if word1 in eng_stopwords:
                dropped.append(word)
            else:
                finalWordList.append(word1)  # No!! put word1 through the usual filter n then decide
            
        elif word[-2:]=="'s":
            word1 = word[0:-3]
            if word1 in eng_stopwords:
                dropped.append(word)
            else:
                finalWordList.append(word1) # No!! put word1 through the usual filter n then decide
            
        elif word[-1]=="'":
            word1 = word[0:-1]
            if word1 in eng_stopwords:
                dropped.append(word)
            else:
                finalWordList.append(word1) # No!! put word1 through the usual filter n then decide
                
        # Now focus on the word
        else:
            # merge hyphenated words, if any
            if re.match(r'\w+(?:-\w+)+', word):
                mergWord = word.replace('-','')
            else:
                mergWord = word
                
            puncFreeWordList = re.findall(r'\w+', mergWord, flags = re.I | re.M) 
            # re.findall uses punctuation as the delimiter and, based on that, returns a list of words.
            # For us, in current set-up, this list will mostly be a one word list but sometimes may 
            # have more than one items, eg. i'm --> [[i],[m]]
            for item in puncFreeWordList:
                if (item in eng_stopwords) | (len(item) <= 1):
                    puncFreeWordList.remove(item)
                    
            "stem and/or lemmatize (decide order) "
            "check alpha or not? -- if numeric/punctuation/spl_chars drop? "
            "check stopwords once again"
            " anything else? "
            [keeps, drops] = filter_words(puncFreeWordList)                   
            
            finalWordList += keeps
            dropped += drops
            
    return [hashtags, contacts, urls, finalWordList, dropped]


    
    
