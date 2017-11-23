import json, math
import re
from nltk.corpus import stopwords
eng_stopwords = stopwords.words('english')
import myStopwords
for sw in myStopwords.STOP_WORDS:
    if sw not in eng_stopwords:
        eng_stopwords.append(sw)


def normalize(text):
    return text.lower().replace("\n", " ")


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
            if re.match(r'\A:[a-z]+:\Z',entry):
                listOfWords_content.append(entry[1:-1])
            elif re.match(r'\A[a-z]+:\Z',entry):
                listOfWords_content.append(entry[0:-1])
            elif re.match(r'\A:[a-z]+\Z',entry):
                listOfWords_content.append(entry[1:])
            elif re.match(r'\w+(?:-\w+)+', entry):
                tmp = entry.replace('-','')
                listOfWords_content.append(tmp)
           # else:
                #print entry
    return [listOfWords_content, listOfWords_dropping]

def tokenize(text):
    words = filter(lambda i: len(i) > 0, normalize(text).replace(',', ' ').replace(';',' ').replace(' " ', ' ').replace('RT',' ').replace('rt', ' ').replace('*',' ').split(' '))
    [words, dropped]  = filter_words(words)
    return words
    


#def getFeatures(js):
#    text = js['text']
#    words = tokenize(text)
#    return words + [
#    "___wordsCount:" + str(len(words)),
#    "___linksCount:" + str(text.count("http://")),
#    "___mentionCount:" + str(text.count("@")),
#    "___hashCount:" + str(text.count("#")),
#    "___source:" + js['source'],
#    "___isRt:" + ("1" if 'rt' in words else "0")
#    ]

def getFeatures(text):
    words = tokenize(text)
    return words #+ [
#    "___wordsCount:" + str(len(words)),
#    "___linksCount:" + str(text.count("http://")),
#    "___mentionCount:" + str(text.count("@")),
#    "___hashCount:" + str(text.count("#")),
#    #"___source:", # + text['source'],
#    "___isRt:" + ("1" if 'rt' in words else "0")
   # ]

def readModel(fileName):
    fp = open(fileName, 'r')
    datum = []
    for x in range(4):
        datum.append(json.loads(fp.readline().strip()))
    fp.close()
    return datum


def writeModel(fileName, docCount, wordSize, wordProb, D):
    fp = open(fileName, 'w')
    fp.write(json.dumps(docCount) + "\n")
    fp.write(json.dumps(wordSize) + "\n")
    fp.write(json.dumps(wordProb) + "\n")
    fp.write(json.dumps(list(D)) + "\n")
    fp.close()


def classify(model, js):
    (docCount, wordSize, wordProb, D) = model
    Gp = Bp = 0;
    for w in getFeatures(js):
        Gp += math.log(conditionalProbability(model, w, 'G'), 2)
        Bp += math.log(conditionalProbability(model, w, 'B'), 2)
        Gp += math.log(float(docCount['G']) / sum(docCount))
        Bp += math.log(float(docCount['B']) / sum(docCount))
        print Gp, " ", Bp
    return "G" if Gp > Bp else "B"


def sum(dict):
    return reduce(lambda x, y: x + y, dict.values())


def conditionalProbability(model, word, klass):
    (docCount, wordSize, wordProb, D) = model
    return float(wordProb[klass].get(word, 0) + 1) / (sum(wordProb[klass]) + len(D))
    
    
