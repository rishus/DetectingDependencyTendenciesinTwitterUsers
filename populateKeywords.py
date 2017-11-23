
import TweetDB as TDB
from EpiPipesApi import *

#counter = 0
#with open('/home/rishu/Courses/CS5525/project/keywordsCosmetics.txt', 'rb') as f:
#    for line in f:
#        lkw = line.split()
#        for kw in lkw:
#            check_id = TDB.session.query(TDB.Keywords).filter(TDB.Keywords.keyword==kw).all()
#            if (len(check_id) == 0):
#                counter += 1
#                u = TDB.Keywords(keyword = kw, id= counter , priority = 1, topic='cosmetics')
#                TDB.session.add(u)
#                print kw
#            else:
#                print kw , 'already present'
#
#
#TDB.session.commit()


#counter=81
#res = scan(TDB.session, filterGT(TDB.session,TDB.Keywords, 'id', 80))
#for r in res:
#        r.id = counter
#        counter = counter + 1
#TDB.session.commit()



#counter = 0
#with open('/home/rishu/Courses/CS5525/project/spam_words.txt', 'rb') as f:
#    for line in f:
#        lkw = line.split()
#        print lkw
#        for kw in lkw: 
#            counter += 1
#            check_id = TDB.session.query(TDB.Spam_words).filter(TDB.Spam_words.word_id==kw).all()
#            if (len(check_id) == 0):
#                u = TDB.Spam_words(word_id = kw, id= counter)
#                TDB.session.add(u)
#                print kw
#            else:
#                print kw , 'already present'
#
#
#TDB.session.commit()


counter = 0
with open('/home/rishu/Courses/CS5525/project/makeupBrands.txt', 'rb') as f:
    for line in f:
        lkw = line.split()
        print lkw
        for kw in lkw: 
            counter += 1
            check_id = TDB.session.query(TDB.Beauty_businesses).filter(TDB.Spam_words.word_id==kw).all()
            if (len(check_id) == 0):
                u = TDB.Spam_words(word_id = kw)
                TDB.session.add(u)
                print kw
            else:
                print kw , 'already present'


TDB.session.commit()

