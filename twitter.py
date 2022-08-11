import tweepy 
import pandas as pd
from tweepy import OAuthHandler
from tweepy import Cursor 
from openpyxl import workbook

"""
Twitter Authentification Credentials
Please update with your own credentials
"""
cons_key = 'cons_key here'
cons_secret = 'cons_secret here'
acc_token = 'acc_token here'
acc_secret = 'acc_secret here'

# (1). Athentication Function
def get_twitter_auth():
    """
    @return:
        - the authentification to Twitter
    """
    try:
        consumer_key = cons_key
        consumer_secret = cons_secret
        access_token = acc_token
        access_secret = acc_secret
        
    except KeyError:
        sys.stderr.write("Twitter Environment Variable not Set\n")
        sys.exit(1)
        
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    return auth
# (2). Client function to access the authentication API
def get_twitter_client():
    """
    @return:
        - the client to access the authentification API
    """
    auth = get_twitter_auth()
    client = tweepy.API(auth, wait_on_rate_limit=True)
    return client
# (3). Function creating final dataframe
def get_tweets_from_user(twitter_user_name, page_limit=16, count_tweet=200):
    """
    @params:
        - twitter_user_name: the twitter username of a user (company, etc.)
        - page_limit: the total number of pages (max=16)
        - count_tweet: maximum number to be retrieved from a page
        
    @return
        - all the tweets from the user twitter_user_name
    """
    client = get_twitter_client()
    
    all_tweets = []
    
    for page in Cursor(client.user_timeline, 
                        screen_name=twitter_user_name, 
                        exclude_replies=True, 
                        count=count_tweet).pages(page_limit):
        for tweet in page:
            parsed_tweet = {}
            parsed_tweet['date'] = tweet.created_at
            parsed_tweet['link'] = tweet.id_str
            parsed_tweet['twitter_name'] = tweet.user.screen_name
            parsed_tweet['text'] = tweet.text
            parsed_tweet['number_of_likes'] = tweet.favorite_count
            parsed_tweet['number_of_retweets'] = tweet.retweet_count
                
            all_tweets.append(parsed_tweet)
    
    # Create dataframe 
    df = pd.DataFrame(all_tweets)
    
    df = df.drop_duplicates( "text" , keep='first')
    df = df[~df.text.str.contains("RT")]
    df = df.reset_index(drop=True)
    df['date'] = df['date'].apply(lambda a: pd.to_datetime(a).date())
    
    return df

PULL = get_tweets_from_user("AstralisLoL") 

PULL.to_excel("Astralis.xlsx")  

print(PULL.head(100))

    






