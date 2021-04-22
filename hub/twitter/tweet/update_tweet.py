import requests
import json
from .token import Token

class UpdateTweet(Token):

    def __init__(self, token, log):
        super().__init__(token, log)

    def create_headers(self):
        return super().create_headers()

    def gather_ids(self):
        return [tweet['id'] for tweet in self.database.find()]

    '''
    id needs to be a list 
    '''
    def update(self, headers, id):

        url = self.create_url(id)
        response = requests.request("GET", url, headers=headers)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        
        print(json.dumps(response.json(), indent=4, sort_keys=True))

    def create_url(self,id):
        # Tweet fields are adjustable. In order to use the extra fields an expansion field is requierd.
        # tweet.fields=lang,author_id
        # tweet_fields = "expansions=referenced_tweets.id,referenced_tweets.id.author_id
        #                 &tweet.fields=author_id,entities,conversation_id,geo,lang,public_metrics,possibly_sensitive
        #                 &user.fields=id,username,name,verified,location"

        tweet_fields = "expansions=author_id,referenced_tweets.id&"
        tweet_fields +="user.fields=id,username,name,verified,location&"
        tweet_fields +="tweet.fields=author_id,"
        tweet_fields += "entities.annotations.probability,entities.annotations.type,entities.annotations.normalized_text"
        tweet_fields += "entities.urls.url,"
        tweet_fields += ",conversation_id,geo,lang,public_metrics,possibly_sensitive"

        # You can adjust ids to include a single Tweets e.g.:
        # ids = "ids=1278747501642657792,1255542774432063488"
        # Or you can add to up to 100 comma-separated IDs
        ids = 'ids=' + ','.join(id)
        ids = "ids=1375074409392697352,1278747501642657792"
        url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
        return url
    
        
#https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets-id
