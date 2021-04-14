import requests
import json
from .token import Token

class UpdateTweet(Token):

    def __init__(self, token, log):
        super().__init__(token, log)
        self.id_list = []

    def gather_ids(self):
        for tweet in self.database.find():
            self.id_list.append(tweet['id'])
        
    def update(self, id):
        response = requests.get(
            "https://api.twitter.com/2/tweets/:id", headers=headers
        )

    def create_headers(self):
        return super().create_headers()

    def create_url(id):
        tweet_fields = "tweet.fields=lang,author_id"
        # Tweet fields are adjustable.
        # Options include:
        # attachments, author_id, context_annotations,
        # conversation_id, created_at, entities, geo, id,
        # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
        # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
        # source, text, and withheld
        ids = "ids=1278747501642657792,1255542774432063488"
        # You can adjust ids to include a single Tweets.
        # Or you can add to up to 100 comma-separated IDs
        url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url
