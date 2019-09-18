# Twitter Flight Deals to SMS Notification Program

### Overview
This program follows specified Twitter accounts and filters live tweets. If those tweets contain certain keywords, the 
tweets are texted to specified phone numbers. 

### Motivation
As a passionate traveler, I avidly follow airline news and flight fares. There are a multitude of Twitter accounts that 
publish flight deals, and I have found Twitter to be one of the best places to find these deals. I signed up to receive
push notifications on my phone using the Twitter app, but I soon realized that I was receiving too many flight deals 
as these Twitter accounts published fares from many different cities and not just the ones I was interested in. My 
initial thought was to create a program that retweeted the flight deals for a specific city. However, after discussing 
the idea with my friends, they convinced me that they would be more likely to use the program if it sent them a text 
message instead of simply retweeting, which would require them to install the Twitter app. 

### Tools
I used Python and the Tweepy library as well as AWS SNS to write this program. I currently have it running on an AWS 
EC2 instance and it has been working without issue. 

### Creating the filters
The following is an example of a file: 
```json
{
  "twitter_account_ids": ["352093320", "other_twitter_ids"],
  "filters": [
    {
      "description": "Los Angeles Flight Deal Tweets",
      "topic_arn": "arn:aws:sns:us-east-1:181202387126:LA_Travel_Deals",
      "search_terms": ["Los Angeles", "LAX", "Burbank", "BUR", "LGB", "ONT"]
    }, 
    {
      "description": "Some description", 
      "topic_arn": "Some sns topic arn", 
      "search_terms": "Terms to search for in tweets"
    }
  ]
}
```
Note that the twitter account ids can be easily found at http://gettwitterid.com/.


### Deployment 
Simply set the following environment variables and run: 

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_REGION_NAME
* TWITTER_CONSUMER_KEY
* TWITTER_CONSUMER_SECRET
* TWITTER_ACCESS_TOKEN
* TWITTER_ACCESS_TOKEN_SECRET

