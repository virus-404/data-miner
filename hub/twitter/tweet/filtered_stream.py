import requests
import os
import json

from datetime import datetime
from .token import Token


class FilteredStream(Token):
    
    def __init__(self,bearer_token, log):      
        super().__init__(bearer_token, log)
        self.__filter = self.__get_filter()
    
    def create_headers(self):
        return super().create_headers()
    
    def __get_filter(self):
        with open('files/filter_word.json', 'r', encoding='utf-8') as file:
            filter = json.load(file)
        self.log.log('Twitter filters are available')
        return filter


    def get_rules(self,headers):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
            )
        self.log.log('Retrieving the rules')
        return response.json()

    def delete_all_rules(self,headers, rules):
        if rules is None or "data" not in rules:
            return None

        ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": ids}}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers=headers,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        self.log.log('Deleting the previously available rules')

    def set_rules(self, headers, delete):
        # You can adjust the rules if needed
        '''
        sample_rules = [
            {"value": "dog has:images", "tag": "dog pictures"},
            {"value": "cat has:images -grumpy", "tag": "cat pictures"},
        ]
        '''
        rules = self.__generate_rules()
        payload = {"add": rules}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers=headers,
            json=payload,
        )
        self.log.log('Setting the new rules')
        if response.status_code != 201:
            self.log.log(json.dumps(response.json()))
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
            )

    def get_stream(self, headers, set):
        self.log.log('Receiving the stream ')
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True,
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                response =  json_response['data']
                self.__database['twitter'].insert_one(response)
                #self.log.log(str(response)) for testing
                
    def __generate_rules(self):
        rules =  []
        file = self.__filter                    

        for item in file['rules']:
            rules.append({'value': item })
        
        return rules

#https://developer.twitter.com/en/docs/twitter-api/rate-limits#v2-limits
