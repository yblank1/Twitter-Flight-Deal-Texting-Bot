import tweepy
from pprint import pprint
import json
import boto3
import os
import logging
import time
import re

CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY'].encode('utf-8')
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET'].encode('utf-8')
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN'].encode('utf-8')
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET'].encode('utf-8')

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_REGION_NAME = os.environ['AWS_REGION_NAME']

class Listener(tweepy.StreamListener):
    def on_status(self, status):

        tweet_data = status._json
        if 'retweeted_status' not in tweet_data and 'quoted_status' not in tweet_data:
            #  Send sms to topic
            for k in filters:
                if k['regex'].search(status.text):
                    client.publish(
                        TopicArn=k['topic_arn'],
                        Message=status.text
                    )


    def on_error(self, status):
        pprint(status)
        logging.error(status)


if __name__ == '__main__':

    # Get the data of the accounts to follow and filters
    with open('config.json', 'r') as f:
        config_data = json.load(f)

    accounts_to_follow = config_data['twitter_account_ids']
    filters = config_data['filters']

    for i in filters:
        i['regex'] = re.compile('|'.join(i['search_terms']), re.IGNORECASE)

    client = boto3.client(
        "sns",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )


    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    while 1:
        try:
            twitter_stream = tweepy.Stream(auth, Listener())
            tc = tweepy.API(auth)
            twitter_stream.filter(follow=accounts_to_follow)
        except Exception as e:
            logging.error(e)
            time.sleep(60)
