
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, String,  PrimaryKeyConstraint, Boolean, Date



conn_str='postgresql+psycopg2://localhost:' + str(5432) + '/makeup'
engine=create_engine(conn_str)

# Name the session and bind the engine to the session
Session = sessionmaker()
Session.configure(bind=engine)
session=Session()
Base = declarative_base()

class Users(Base):
     __tablename__ = 'users'
     id = Column(BigInteger, primary_key=True)
#     followers_count = Column(Integer)
#     friends_count = Column(Integer)
     location = Column(String)  # can be falsely reported
#     following = Column(String)
     name = Column(String)
     screen_name = Column(String)
     created_at = Column(String)
     language = Column(String)
     verified = Column(String)
     url = Column(String)
   
class Tweet_mirror(Base):
    __tablename__='tweet_mirror'
    tid=Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)

class Tweet_time(Base):
    __tablename__='tweet_time'
    tweet_id=Column(BigInteger, primary_key=True)
    date=Column(Date)
#Tweet version v3 which has place as an attribute

class User_vs_class(Base):
    __tablename__ = 'user_vs_class'
    user_id = Column(BigInteger, primary_key=True)
    followers_count = Column(Integer)
    cl = Column(String)

class Tweet(Base):
    __tablename__='tweet'
    id=Column(BigInteger, primary_key=True)
    text = Column(String)
    created_at = Column(String)
    tweet_coords=Column(String)      # latitude-longitude of tweet location (nullifiable)
    place = Column(String)           # bounding box for places associated with/ mentioned in the tweet location as reported by the device (nullifiable)
    isRT = Column(Integer)
    retweeted = Column(Boolean)
    user_id = Column(BigInteger)     # unique   
    language = Column(String)
    
    contributors = Column(String)
    truncated = Column(Boolean)
    in_reply_to_status_id = Column(String)
    in_reply_to_screen_name = Column(String)
    in_reply_to_user_id=Column(String)
    in_reply_to_user_id_str=Column(String)
    in_reply_to_status_id_str=Column(String)
    favorite_count = Column(Integer)
    source = Column(String)
    favorited=Column(Boolean)
    id_str=Column(String)
    retweet_count=Column(Integer)
    

class Processed_tweet(Base):
    __tablename__ = 'processed_tweet'
    tweet_id = Column(Integer, primary_key=True)
     
class Hashtags(Base):
     __tablename__ = 'hashtags'
     id = Column(Integer)
     hashtag = Column(Integer, primary_key=True)
     
class Words(Base):
    __tablename__='words'
    word = Column(String, primary_key=True)
    id = Column(Integer)
    
class Keywords(Base):
    __tablename__='keywords'
    keyword = Column(String, primary_key=True)
    id = Column(Integer)
    priority = Column(Integer, primary_key=True)
    topic = Column(String)
    
class Words_in_tweet(Base):
    __tablename__='words_in_tweet'
    rec_id  = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(BigInteger)
    word_id=Column(String)
    #__table_args__ = (
    #    PrimaryKeyConstraint('tweet_id', 'word_id'),
    #    {},
    #)

class Shopping_keywords(Base):
    __tablename__='shopping_keywords'
    m_word_id = Column(String, primary_key=True)

class Regret_keywords(Base):
    __tablename__='regret_keywords'
    m_word_id = Column(String, primary_key=True)
    
#class Shopping_keywords_view(Base):
#    __tablename__='m_shopping_keywords'
#    m_word_id = Column(String, primary_key=True)
#    __table_args__ = {'extend_existing':True}

class Hashtag_in_tweet(Base):
    __tablename__='hashtag_in_tweet'
    hash_id = Column(Integer)
    tweet_id = Column(Integer)
    topic = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint('hash_id', 'tweet_id'),
        {},
    )
    
class Network(Base):
    __tablename__='network'
    topic = Column(String)
    tweet_id = Column(BigInteger)
    src_id = Column(BigInteger)   #user_id = Column(BigInteger)
    des_id = Column(BigInteger)   #u2_id = Column(String)
    connect = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint('topic','tweet_id', 'src_id', 'des_id'),
        {},
    )
    
class Topic_tweetid(Base):
    __tablename__ = 'topic_tweetid'
    topic = Column(String)
    tweet_id = Column(BigInteger)
    __table_args__ = (
        PrimaryKeyConstraint('topic', 'tweet_id'),
        {},
    )

class User_timeline(Base):
    __tablename__ = 'user_timeline'
    user_id = Column(BigInteger)
    tweet_id = Column(BigInteger)
    date_time_str = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'tweet_id'),
        {},
    )

class User_followees(Base):
    __tablename__ = 'user_followers'
    user_id = Column(BigInteger)
    followee_id = Column(BigInteger)
    followeeFollowers_count = Column(BigInteger)
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'followee_id'),
        {},
    )
    
class Spam_words(Base):
    __tablename__ = 'spam_words'
    word_id = Column(String, primary_key=True)
    id = Column(Integer)

    
class Spam_tweet(Base):
    __tablename__ = 'spam_tweet'
    tweet_id = Column(BigInteger, primary_key = True)
    text = Column(String)
    cl = Column(String)
    spammer_id = Column(BigInteger)
    spammer_name = Column(String)

class Beauty_tweet(Base):
    __tablename__ = 'beauty_tweet'
    tweet_id = Column(BigInteger, primary_key = True)
    text = Column(String)
    cl = Column(String)
    user_id = Column(BigInteger)
    user_screen_name = Column(String)
    
class User_vs_company(Base):
    __tablename__ = 'user_vs_company'
    user_id = Column(BigInteger)
    company_id = Column(BigInteger)
    company_screen_name = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'company_id'),
        {},
    )
    
class Businesses(Base):
    __tablename__ = 'businesses'
    biz_id = Column(BigInteger, primary_key=True)
    biz_followers_count = Column(Integer)
#     friends_count = Column(Integer)
    biz_location = Column(String)  # can be falsely reported
#     following = Column(String)
    biz_name = Column(String)
    biz_screen_name = Column(String)
    biz_created_at = Column(String)
    biz_language = Column(String)
    biz_verified = Column(String)
    biz_url = Column(String)


class Beauty_businesses(Base):
    __tablename__ = 'beauty_businesses'
    biz_screen_name = Column(String, primary_key = True)
    
class Beautybiz_training_vocab(Base):
    __tablename__='beautybiz_training_vocab'
    rec_id  = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(BigInteger)
    word_id=Column(String)
    cl = Column(String)
    
class Beautybiz_training_tweet(Base):
    __tablename__='beautybiz_training_tweet' 
    tweet_id=Column(BigInteger, primary_key=True)
    text = Column(String)
    created_at = Column(String)
    tweet_coords=Column(String)      # latitude-longitude of tweet location (nullifiable)
    place = Column(String)           # bounding box for places associated with/ mentioned in the tweet location as reported by the device (nullifiable)
    isRT = Column(Integer)
    retweeted = Column(Boolean)
    user_id = Column(BigInteger)     # unique   
    language = Column(String)
    cl = Column(String)

class Beautytweet_training_tweet(Base):
    __tablename__='beautytweet_training_tweet' 
    tweet_id=Column(BigInteger, primary_key=True)
    text = Column(String)
    cl = Column(String)

class Spamtweet_training_tweet(Base):
    __tablename__='spamtweet_training_tweet' 
    tweet_id=Column(BigInteger, primary_key=True)
    text = Column(String)
    cl = Column(String)

class Celebrities(Base):
    __tablename__ = 'celebrities'
    celeb_id = Column(BigInteger, primary_key=True)
    celeb_followers_count = Column(Integer)
#     followers_count = Column(Integer)
#     friends_count = Column(Integer)
    celeb_location = Column(String)  # can be falsely reported
#     following = Column(String)
    celeb_name = Column(String)
    celeb_screen_name = Column(String)
    celeb_created_at = Column(String)
    celeb_language = Column(String)
    celeb_verified = Column(String)
    celeb_url = Column(String)


class Dependency_analysis(Base):
     __tablename__='dependency_analysis'
     user_id = Column(BigInteger, primary_key=True)
     num_biz_following = Column(Integer)

     bt = Column(Integer)
     rt = Column(Integer)
     st = Column(Integer)
     mt = Column(Integer)
     ot = Column(Integer) # other tweets
     snst = Column(Integer)
     btor = Column(Integer)
     btos = Column(Integer)
     btom = Column(Integer)
     btosns = Column(Integer)
     stor = Column(Integer)
     mtor = Column(Integer)


#class User(Base):
#     __tablename__ = 'users'
#     id = Column(BigInteger, primary_key=True)
#     followers_count = Column(Integer)
#     friends_count = Column(Integer)
#     location = Column(String)  # can be falsely reported
#     following = Column(String)
#     name = Column(String)
#     created_at = Column(String)
     
     
#def scan(session, object):
#    return session.query(object).all()
    
    

#kwi = keywords(kw, 1)
#session.add(kwi)
#Base.metadata.create_all(engine)
#
#session.commit()
