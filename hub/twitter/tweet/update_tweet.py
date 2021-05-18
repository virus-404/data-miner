import requests
import json
from ftfy import fix_text
import copy
from .token import Token

class UpdateTweet(Token):

    def __init__(self, token, log):
        super().__init__(token, log)

    def create_headers(self):
        return super().create_headers()

    def gather_ids(self):
        #return [tweet['id'] for tweet in self.database['twitter'].find()] #all
        return [tweet['id'] for tweet in self.database['twitter'].find(
            {
                'time-stamp': {'$exists': True}
            }
        )] #only new ones

    '''
    id needs to be a list 
    '''
    def update(self, headers, id):
        url = self.create_url(id)
        response = requests.request('GET', url, headers=headers)

        if response.status_code != 200:
            raise Exception(
                'Request returned an error: {} {}'.format(
                    response.status_code, response.text
                )
            )

        response = self.parse_json(response.text)
        # print(json.dumps(response, indent=4, sort_keys=False)) For testing
        if response == {}: 
            return
       
        try:
            for tweet in response['tweets']:
                self.database['twitter'].replace_one(
                    filter = {'id': tweet['id']},
                    replacement = tweet,
                    upsert = True
                )
            
            for user in response['users']:
                self.database['twitter_users'].replace_one(
                    filter = {'id': user['id']},
                    replacement = user, 
                    upsert = True
                )
        except:
            var = traceback.format_exc()
            print(var)
    
       
    def parse_json(self,response):
        response = json.loads(response)
        not_wanted = ['end', 'start', 'display_url', 'errors',
                              'expanded_url', 'images', 'height', 'status', 'unwound_url']
        items = self.delete_items(response, not_wanted)
        res = {}

        if 'data' in items.keys(): 
            res['tweets'] = items['data'] 
            res['users'] = items['includes']['users']
            if 'tweets' in items['includes'].keys():
                res['tweets'] += items['includes']['tweets']

        return res

    def delete_items(self,items, del_list):
        if isinstance(items, dict):
            cp = copy.deepcopy(items)
            for key in cp.keys():
                if key in del_list:
                    del items[key]
                else:
                    items[key] = self.delete_items(items[key], del_list)
        elif isinstance(items, list):
            for i in range(len(items)):
                items[i] = self.delete_items(items[i], del_list)
                if not items[i]:
                    del items[i]
        return items

    def create_url(self,id):
        # Tweet fields are adjustable. 
        # tweet.fields=lang,author_id

        tweet_fields =  'expansions=referenced_tweets.id,referenced_tweets.id.author_id'
        tweet_fields += '&tweet.fields=author_id,conversation_id,created_at,entities,geo,in_reply_to_user_id,lang,possibly_sensitive,public_metrics'
        tweet_fields += '&user.fields=id,username,name,verified,location'

        # You can adjust ids to include a single Tweets e.g.:
        # ids = 'ids=1278747501642657792,1255542774432063488'
        # Or you can add to up to 100 comma-separated IDs
        ids = 'ids=' + ','.join(id)
        url = 'https://api.twitter.com/2/tweets?{}&{}'.format(ids, tweet_fields)
        return url
  
#https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets-id
