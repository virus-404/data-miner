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

        import sys
        url = self.create_url(id)
        print(url)
        sys.exit()
        response = requests.request("GET", url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        self.log.log(str(response))  # for testing

    def create_url(self,id):
        # Tweet fields are adjustable.
        # Options include:
        # attachments, author_id, context_annotations,
        # conversation_id, created_at, entities, geo, id,
        # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
        # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
        # source, text, and withheld
        tweet_fields = "tweet.fields=lang,author_id"
        # You can adjust ids to include a single Tweets e.g.:
        # "ids=1278747501642657792,1255542774432063488"
        # Or you can add to up to 100 comma-separated IDs
        ids = 'ids=' + ','.join(id)
        url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
        return url
    
        
#https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets-id
